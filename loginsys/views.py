from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from news.models import News
from django.contrib.auth.models import User

def login(request):
   context={}
   context.update(csrf(request))
   context['departments']=News.departments
   if(request.POST):
      username=request.POST.get('username','')
      password=request.POST.get('password','')
      user=auth.authenticate(username=username,password=password)
      if user is not None:
         auth.login(request, user)
         return redirect('/')
      else:
         login_error = "Authentication problem: user is not found."
         context['login_error'] = login_error
         return render(request,'login.html', context)
   else:
      return render(request,'login.html', context)

def logout(request):
   auth.logout(request)
   return redirect('/')

def register(request):
   context = {}
   context.update(csrf(request))
   context['departments'] = News.departments
   if (request.POST):
      email = request.POST.get('email','')
      username = request.POST.get('username', '')
      password1 = request.POST.get('password1', '')
      password2= request.POST.get('password2','')
      if password1 is not '' and username is not '' and not User.objects.filter(username=username).exists() and \
                      password1 == password2 and not User.objects.filter(email=email).exists():
         User.objects.create_user(email=email, username=username, password=password1)
         if User is not None:
            return redirect('http://127.0.0.1:8000/succesful_registration/')
         else:
            context['registration_error']='Invalid data was entered.'
            return render(request,'register.html', context)
      elif User.objects.filter(username=username).exists():
         context['registration_error'] = 'User with such username already exists.'
         return render('request,register.html', context)
      elif email=='':
          context['registration_error']='Email field is required'
          return render('register.html', context)
      elif username=='':
          context['registration_error']='Username field is required'
          return render(request,'register.html', context)
      elif password1=='':
          context['registration_error']='Password field is required'
          return render(request,'register.html', context)
      elif User.objects.filter(email=email).exists():
          context['registration_error']='User with such email already exists.'
          return render(request,'register.html', context)
      elif password1!=password2:
         context['registration_error']='Passwords dont match.'
         return render(request,'register.html', context)
   else:
      return render(request,'register.html', context)



# Create your views here.
