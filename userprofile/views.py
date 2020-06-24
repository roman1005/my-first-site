from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProfileForm
from .models import UserHomePage
from django.contrib import auth
from django.contrib.auth.models import User
from news.models import News
from django.template.context_processors import csrf
from news.views import  is_CM

def create_profile(request):
    context={}
    context.update(csrf(request))
    context['departments']=News.departments
    username = auth.get_user(request).username
    context['username']=username
    if request.POST:
        form=ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = User.objects.get(username=username)
            profile.save()
            return redirect('/profile/' + username + '/')
        else:
            if (context['username']):
                user = User.objects.get(username=auth.get_user(request).username)
                context['C_M'] = is_CM(user)
            else:
                context['C_M'] = None
            context['form']=ProfileForm()
            context['creation_error']="Invalid data was entered."
            return render(request,'profile_create.html', context)
    else:
        if (context['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            context['C_M'] = is_CM(user)
        else:
            context['C_M'] = None
        context['form']=ProfileForm()
        return render(request, 'profile_create.html', context)


def update_profile(request):
    context={}
    context['departments'] = News.departments
    context.update(csrf(request))
    username = auth.get_user(request).username
    context['username'] = username
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
            if (context['username']):
                user = User.objects.get(username=auth.get_user(request).username)
                context['C_M'] = is_CM(user)
            else:
                context['C_M'] = None
            context['update_error']="Invalid data entered."
            context['form']=form
            return render( 'profile_update.html', context)
    else:
        if (context['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            context['C_M'] = is_CM(user)
        else:
            context['C_M'] = None
        context['form'] = form
        return render(request, 'profile_update.html', context)


def view_profile(request, username):
    context={}
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
        context['profile']=profile
    context['host_user']=host_user
    context['username']=username
    context['departments']=News.departments
    context['username']=auth.get_user(request)
    if (context['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        context['C_M'] = is_CM(user)
    else:
        context['C_M'] = None
    return render(request,'view_profile.html', context)
# Create your views here.
