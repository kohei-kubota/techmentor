from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^mentor/(?P<id>[0-9]+)/$', views.mentor_detail, name='mentor_detail'),
    url(r'^mentor_list/$', views.mentor_list, name='mentor_list'),
    url(r'^edit_mentor/$', views.edit_mentor, name='edit_mentor'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^my_skill/$', views.my_skills, name='my_skills'),
    url(r'^edit_skill/edit/(?P<id>[0-9]+)/$', views.edit_skill, name="edit_skill"),
    url(r'^category/(?P<link>[\w|-]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_skill/$', views.add_skill, name='add_skill'),
    url(r'^mentor/reserve/(?P<id>[0-9]+)/$', views.reserve, name='reserve'),
    url(r'^my_schedule/$', views.my_schedule, name='my_schedule'),
    url(r'^edit_schedule/(?P<id>[0-9]+)/$', views.edit_schedule, name='edit_schedule'),
    url(r'^create_schedule/$', views.create_schedule, name='create_schedule'),
    url(r'^mentor/reserve_check/(?P<id>[0-9]+)/(?P<mentor>[0-9]+)/$', views.reserve_check, name='reserve_check'),
    url(r'^thanks_page/$', views.thanks_page, name='thanks_page'),
    url(r'^infomation/$', views.infomation, name='infomation'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^company/$', views.company, name='company'),
    url(r'^privacy_policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^policy/$', views.policy, name='policy'),
]