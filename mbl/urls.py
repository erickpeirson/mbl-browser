"""mbl URL Configuration"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from browser import views
from browser import rest

router = routers.DefaultRouter()
router.register(r'coursegroups', rest.CourseGroupViewSet)
router.register(r'courses', rest.CourseViewSet)
router.register(r'people', rest.PersonViewSet)
router.register(r'institutions', rest.InstitutionViewSet)
router.register(r'locations', rest.LocationViewSet)
router.register(r'position', rest.LocationViewSet)


urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="home"),
    url(r'^bulk/(?P<model>[a-z]+)/$', views.bulk_action, name="bulk-action"),

    url(r'^course/(?P<course_id>[0-9]+)/$', views.course, name="course"),
    url(r'^course/(?P<course_id>[0-9]+)/delete/$', views.course_delete, name="delete-course"),
    url(r'^course/(?P<course_id>[0-9]+)/edit/$', views.edit_course, name="edit-course"),
    url(r'^course/(?P<course_id>[0-9]+)/add/$', views.attendee_create, name="add-attendee"),
    url(r'^course/$', views.course, name="courses"),
    url(r'^course/create/$', views.course_create, name="create-course-nogroup"),
    url(r'^person/(?P<person_id>[0-9]+)/$', views.person, name="person"),
    url(r'^person/(?P<person_id>[0-9]+)/edit/$', views.edit_person, name="edit-person"),
    url(r'^person/(?P<person_id>[0-9]+)/split/$', views.split_person, name="split-person"),
    url(r'^person/merge/$', views.merge_people, name="merge-people"),
    url(r'^person/$', views.person, name="person_list"),
    url(r'^person/(?P<person_id>[0-9]+)/investigator/add/$',views.add_investigator_record,name='add-investigator'),
    url(r'^person/(?P<person_id>[0-9]+)/investigator/(?P<research_id>[0-9]+)/edit/$',views.edit_investigator_record,name='edit-investigator'),
    url(r'^person/(?P<person_id>[0-9]+)/investigator/(?P<research_id>[0-9]+)/delete/$', views.delete_investigator_record, name='delete-investigator'),
    url(r'^person/(?P<person_id>[0-9]+)/position/add/$', views.add_position, name='add-position'),
    url(r'^person/(?P<person_id>[0-9]+)/position/(?P<position_id>[0-9]+)/edit/$', views.edit_position, name='edit-position'),
    url(r'^person/(?P<person_id>[0-9]+)/position/(?P<position_id>[0-9]+)/delete/$', views.delete_position, name='delete-position'),
    url(r'^institution/(?P<institution_id>[0-9]+)/$', views.institution, name="institution"),
    url(r'^institution/(?P<institution_id>[0-9]+)/edit/$', views.edit_institution, name="edit-institution"),
    url(r'^institution/$', views.institution, name="institution_list"),

    url(r'^location/(?P<location_id>[0-9]+)/$', views.location, name="location"),
    url(r'^location/(?P<location_id>[0-9]+)/edit/$', views.edit_location, name="edit-location"),
    url(r'^location/(?P<location_id>[0-9]+)/split/$', views.split_location, name="split-location"),
    url(r'^location/$', views.location, name="location_list"),

    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/$', views.coursegroup, name="coursegroup"),
    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/edit/$', views.edit_coursegroup, name="edit-coursegroup"),
    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+).json$', views.coursegroup_data, name="coursegroup_data"),
    url(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/create/$', views.course_create, name="create-course"),
    url(r'^coursegroup/$', views.coursegroup, name="coursegroup_list"),
    url(r'^about/$', views.about, name="about"),
    url(r'^search/$', views.generic_autocomplete, name="search"),

    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
