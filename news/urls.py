from django.conf.urls import url
from news.views import home, news_detail, news_list, general_tags_news, department_list, add_comment, success_reg

urlpatterns = [
    url(r'^add/comment/(?P<news>[-\w]+)/', add_comment, name='add_comment'),
    url(r'^news/(?P<news>[-\w]+)/', news_detail, name='news_detail'),
    url(r'^all/', news_list, name='news_list'),
    url(r'^news_with_tag/(?P<tag>[-\w]+)/',  general_tags_news, name=' general_tags_news'),
    url(r'^home/', home, name='home'),
    url(r'^department=(?P<department>[-\w]+)/',  department_list, name=' department_list'),
    url(r'^succesful_registration/', success_reg, name='success_reg'),
    url(r'^$', home, name='home'),
]