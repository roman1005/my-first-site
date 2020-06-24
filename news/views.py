from django.shortcuts import render, get_object_or_404, redirect
from news.models import News, Paragraph, Tag, Comment
from news.forms import CommentForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User, Group
departments=News.departments

def is_CM(user):
    is_CM = user.groups.filter(name="ContentManagers").exists()
    return is_CM


def home(request):
   all=News.objects.all()
   news=all[:5]
   context={}
   context['username'] = auth.get_user(request).username
   if (context['username']):
       user = User.objects.get(username=auth.get_user(request).username)
       context['C_M'] = is_CM(user)
   else:
       context['C_M'] = None
   context['username']=auth.get_user(request).username
   context['news']=news
   context['departments'] = departments
   return render(request, 'news_list.html', context)


def news_list(request):
    news=News.objects.all()
    context={}
    context['username'] = auth.get_user(request).username
    if (context['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        context['C_M'] = is_CM(user)
    else:
        context['C_M'] = None
    context['username'] = auth.get_user(request).username
    context['news']=news
    context['departments']=departments
    return render(request,'news_list.html', context )


def department_list(request,department):
    context={}
    context['username'] = auth.get_user(request).username
    if (context['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        context['C_M'] = is_CM(user)
    else:
        context['C_M'] = None
    context['username'] = auth.get_user(request).username
    news=News.objects.filter(department=department)
    context['news']=news
    context['departments'] = departments
    return render(request,'news_list.html', context)


def news_detail(request, news):
    context={}
    news= get_object_or_404(News, slug=news)
    context['news']=news
    context['username'] = auth.get_user(request).username
    if (context['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        context['C_M'] = is_CM(user)
    else:
        context['C_M'] = None
    context.update(csrf(request))
    paragraphs = Paragraph.objects.filter(news_paragraph_id=news.id)
    comments=Comment.objects.filter(comments_news_id=news.id)
    context['comments'] = comments
    context['paragraphs'] = paragraphs
    context['tags'] = Tag.objects.filter(news_tag_id=news.id)
    context['departments']=departments
    return render(request, 'news_detail.html', context)


def general_tags_news(request, tag):
    context={}
    context['username'] = auth.get_user(request).username
    if (context['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        context['C_M'] = is_CM(user)
    else:
        context['C_M'] = None
    news=list()
    for i in range(0,len(Tag.objects.filter(tag=tag))):
        k=News.objects.get(id=Tag.objects.filter(tag=tag)[i].news_tag_id)
        news.append(k)
    context['departments']=departments
    context['news']=news
    return render(request,'news_list.html', context)


def add_comment(request, news):
    context={}
    context.update(csrf(request))
    if request.POST:
        form=CommentForm(request.POST)
        new=News.objects.get(slug=news)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.comments_user=request.user
            comment.comments_news_id=new.id
            comment.published_time=timezone.now()
            comment.save()
            return redirect('/news/'+news+'/')
        else:
            form = CommentForm()
            context['form']=form
            context['creation_error']="Invalid information was entered."
            return render(request,'add_comment.html',context)
    else:
        context['username'] = auth.get_user(request).username
        if (context['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            context['C_M'] = is_CM(user)
        else:
            context['C_M'] = None
        context['form'] = CommentForm()
        context['news'] = news
        context['departments']=departments
        return render(request, 'add_comment.html', context)

def success_reg(request):
    context = {}
    context['username'] = ''
    context['departments']=departments
    return render(request,'succes_reg.html', context)
# Create your views here.
