from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .forms import ProfileForm
from .models import UserHomePage
from django.contrib import auth
from django.contrib.auth.models import User
from news.models import News
from django.template.context_processors import csrf
from news.views import  is_CM

def create_profile(request):
    args={}
    args.update(csrf(request))
    args['departments']=News.departments
    username = auth.get_user(request).username
    args['username']=username
    if request.POST:
        form=ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = User.objects.get(username=username)
            profile.save()
            return redirect('/profile/' + username + '/')
        else:
            if (args['username']):
                user = User.objects.get(username=auth.get_user(request).username)
                args['C_M'] = is_CM(user)
            else:
                args['C_M'] = None
            args['form']=ProfileForm()
            args['creation_error']="Invalid data was entered."
            return render_to_response('profile_create.html', args)
    else:
        if (args['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            args['C_M'] = is_CM(user)
        else:
            args['C_M'] = None
        args['form']=ProfileForm()
        return render(request, 'profile_create.html', args)


def update_profile(request):
    args={}
    args['departments'] = News.departments
    args.update(csrf(request))
    username = auth.get_user(request).username
    args['username'] = username
    if UserHomePage.objects.filter(user_id=User.objects.get(username=username)).exists():
        profile=UserHomePage.objects.get(user_id=User.objects.get(username=username))
    form = ProfileForm(request.POST or None,
                        request.FILES or None, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
           profile=form.save(commit=False)
           profile.user=User.objects.get(username=username)
           profile.save()
           return redirect('/profile/'+username+'/')
        else:
            if (args['username']):
                user = User.objects.get(username=auth.get_user(request).username)
                args['C_M'] = is_CM(user)
            else:
                args['C_M'] = None
            args['update_error']="Invalid data entered."
            args['form']=form
            return render_to_response( 'profile_update.html', args)
    else:
        if (args['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            args['C_M'] = is_CM(user)
        else:
            args['C_M'] = None
        args['form'] = form
        return render(request, 'profile_update.html', args)


def view_profile(request, username):
    args={}
    profile_user=User.objects.get(username=username)
    if auth.get_user(request).username!=username:
        host_user=None
    else:
        host_user=1
    id=profile_user.id
    if UserHomePage.objects.filter(user_id=id).exists():
        profile=UserHomePage.objects.get(user_id=id)
    else:
        profile=None
    if profile is not None:
        args['profile']=profile
    args['host_user']=host_user
    args['username']=username
    args['departments']=News.departments
    args['username']=auth.get_user(request)
    if (args['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        args['C_M'] = is_CM(user)
    else:
        args['C_M'] = None
    return render_to_response('view_profile.html', args)
# Create your views here.
