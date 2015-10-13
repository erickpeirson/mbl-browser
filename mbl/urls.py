"""mbl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from browser import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="home"),
    url(r'^course/(?P<course_id>[0-9]+)/$', views.course, name="course"),
    url(r'^course/$', views.course, name="course_list"),
    url(r'^person/(?P<person_id>[0-9]+)/$', views.person, name="person"),
    url(r'^person/$', views.person, name="person_list"),
    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/$', views.coursegroup, name="coursegroup"),
    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+).json$', views.coursegroup_data, name="coursegroup_data"),
    url(r'^coursegroup/$', views.coursegroup, name="coursegroup_list"),
]
