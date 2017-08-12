from django.shortcuts import render, get_object_or_404, redirect, render_to_response
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
   args={}
   args['username'] = auth.get_user(request).username
   if (args['username']):
       user = User.objects.get(username=auth.get_user(request).username)
       args['C_M'] = is_CM(user)
   else:
       args['C_M'] = None
   args['username']=auth.get_user(request).username
   args['news']=news
   args['departments'] = departments
   return render(request, 'news_list.html', args)


def news_list(request):
    news=News.objects.all()
    args={}
    args['username'] = auth.get_user(request).username
    if (args['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        args['C_M'] = is_CM(user)
    else:
        args['C_M'] = None
    args['username'] = auth.get_user(request).username
    args['news']=news
    args['departments']=departments
    return render(request,'news_list.html', args )


def department_list(request,department):
    args={}
    args['username'] = auth.get_user(request).username
    if (args['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        args['C_M'] = is_CM(user)
    else:
        args['C_M'] = None
    args['username'] = auth.get_user(request).username
    news=News.objects.filter(department=department)
    args['news']=news
    args['departments'] = departments
    return render(request,'news_list.html', args)


def news_detail(request, news):
    args={}
    news= get_object_or_404(News, slug=news)
    args['news']=news
    args['username'] = auth.get_user(request).username
    if (args['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        args['C_M'] = is_CM(user)
    else:
        args['C_M'] = None
    args.update(csrf(request))
    paragraphs = Paragraph.objects.filter(news_paragraph_id=news.id)
    comments=Comment.objects.filter(comments_news_id=news.id)
    args['comments'] = comments
    args['paragraphs'] = paragraphs
    args['tags'] = Tag.objects.filter(news_tag_id=news.id)
    args['departments']=departments
    return render(request, 'news_detail.html', args)


def general_tags_news(request, tag):
    args={}
    args['username'] = auth.get_user(request).username
    if (args['username']):
        user = User.objects.get(username=auth.get_user(request).username)
        args['C_M'] = is_CM(user)
    else:
        args['C_M'] = None
    news=list()
    for i in range(0,len(Tag.objects.filter(tag=tag))):
        k=News.objects.get(id=Tag.objects.filter(tag=tag)[i].news_tag_id)
        news.append(k)
    args['departments']=departments
    args['news']=news
    return render(request,'news_list.html', args)


def add_comment(request, news):
    args={}
    args.update(csrf(request))
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
            args['form']=form
            args['creation_error']="Invalid information was entered."
            return render_to_response('add_comment.html',args)
    else:
        args['username'] = auth.get_user(request).username
        if (args['username']):
            user = User.objects.get(username=auth.get_user(request).username)
            args['C_M'] = is_CM(user)
        else:
            args['C_M'] = None
        args['form'] = CommentForm()
        args['news'] = news
        args['departments']=departments
        return render(request, 'add_comment.html', args)

def success_reg(request):
    args = {}
    args['username'] = ''
    args['departments']=departments
    return render(request,'succes_reg.html', args)
# Create your views here.
