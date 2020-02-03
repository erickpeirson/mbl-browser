"""mbl URL Configuration"""
from django.urls import include, re_path
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


urlpatterns = [
    re_path('', include('social.apps.django_app.urls', namespace='social')),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.home, name="home"),
    re_path(r'^bulk/(?P<model>[a-z]+)/$', views.bulk_action, name="bulk-action"),

    re_path(r'^course/(?P<course_id>[0-9]+)/$', views.course, name="course"),
    re_path(r'^course/(?P<course_id>[0-9]+)/delete/$', views.course_delete, name="delete-course"),
    re_path(r'^course/(?P<course_id>[0-9]+)/edit/$', views.edit_course, name="edit-course"),
    re_path(r'^course/(?P<course_id>[0-9]+)/add/$', views.attendee_create, name="add-attendee"),
    re_path(r'^course/$', views.course, name="courses"),
    re_path(r'^course/create/$', views.course_create, name="create-course-nogroup"),
    re_path(r'^person/(?P<person_id>[0-9]+)/$', views.person, name="person"),
    re_path(r'^person/(?P<person_id>[0-9]+)/edit/$', views.handle_person, name="edit-person"),
    re_path(r'^person/(?P<person_id>[0-9]+)/split/$', views.split_person, name="split-person"),
    re_path(r'^person/merge/$', views.merge_people, name="merge-people"),
    re_path(r'^person/$', views.person, name="person_list"),
    re_path(r'^person/add/$', views.handle_person, name="add-person"),
    re_path(r'^person/(?P<person_id>[0-9]+)/investigator/add/$',views.add_investigator_record,name='add-investigator'),
    re_path(r'^person/(?P<person_id>[0-9]+)/investigator/(?P<research_id>[0-9]+)/edit/$',views.edit_investigator_record,name='edit-investigator'),
    re_path(r'^person/(?P<person_id>[0-9]+)/investigator/(?P<research_id>[0-9]+)/delete/$', views.delete_investigator_record, name='delete-investigator'),
    re_path(r'^person/(?P<person_id>[0-9]+)/affiliation/(?P<affiliation_id>[0-9]+)/edit/$', views.edit_affiliation, name='edit-affiliation'),
    re_path(r'^person/(?P<person_id>[0-9]+)/affiliation/(?P<affiliation_id>[0-9]+)/delete/$', views.delete_affiliation_record, name='delete-affiliation'),
    re_path(r'^person/(?P<person_id>[0-9]+)/position(?:/(?P<position_id>[0-9]+))?/$', views.position, name='position'),
    re_path(r'^person/(?P<person_id>[0-9]+)/position/(?P<position_id>[0-9]+)/delete/$', views.delete_position, name='delete-position'),
    re_path(r'^institution/(?P<institution_id>[0-9]+)/$', views.institution, name="institution"),
    re_path(r'^institution/(?P<institution_id>[0-9]+)/edit/$', views.edit_institution, name="edit-institution"),
    re_path(r'^institution/$', views.institution, name="institution_list"),

    re_path(r'^location/(?P<location_id>[0-9]+)/$', views.location, name="location"),
    re_path(r'^location/(?P<location_id>[0-9]+)/edit/$', views.edit_location, name="edit-location"),
    re_path(r'^location/(?P<location_id>[0-9]+)/split/$', views.split_location, name="split-location"),
    re_path(r'^location/$', views.location, name="location_list"),

    re_path(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/$', views.coursegroup, name="coursegroup"),
    re_path(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/edit/$', views.edit_coursegroup, name="edit-coursegroup"),
    re_path(r'^coursegroup/(?P<coursegroup_id>[0-9]+).json$', views.coursegroup_data, name="coursegroup_data"),
    re_path(r'^coursegroup/(?P<coursegroup_id>[0-9]+)/create/$', views.course_create, name="create-course"),
    re_path(r'^coursegroup/$', views.coursegroup, name="coursegroup_list"),
    re_path(r'^about/$', views.about, name="about"),
    re_path(r'^search/$', views.generic_autocomplete, name="search"),

    re_path(r'^rest/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
