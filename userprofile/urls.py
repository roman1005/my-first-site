from django.conf.urls import url
from userprofile.views import create_profile, update_profile, view_profile

urlpatterns = [
    url(r'create/', create_profile, name='create_profile'),
    url(r'^update/',  update_profile, name='update_profile'),
    url(r'^(?P<username>[-\w]+)/', view_profile, name='view_profile'),
]