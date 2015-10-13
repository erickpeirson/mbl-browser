from django.contrib import admin
from browser.models import *


class PartOfInline(admin.TabularInline):
    model = PartOf
    readonly_fields = ('year', 'course', 'coursegroup')
    extra = 0
    can_delete = False
    list_sort = ('year',)


class AttendanceInline(admin.TabularInline):
    model = Attendance
    readonly_fields = ('year', 'person', 'course', 'role')
    extra = 0
    can_delete = False


class AffiliationInline(admin.TabularInline):
    model = Affiliation
    readonly_fields = ('year', 'person', 'institution', 'position')
    extra = 0
    can_delete = False


class LocationInline(admin.TabularInline):
    model = Location
    can_delete = False
    extras = 0


class AttendanceInline(admin.TabularInline):
    model = Attendance
    readonly_fields = ('person', 'course', 'role', 'year')
    extra = 0
    can_delete = False


class InvestigatorInline(admin.TabularInline):
    model = Investigator
    readonly_fields = ('person', 'subject', 'role', 'year')
    extra = 0
    can_delete = False


class LocalizationInline(admin.TabularInline):
    model = Localization
    readonly_fields = ('person', 'location', 'year')
    extra = 0
    can_delete = False

## ModelAdmins ##

class PersonAdmin(admin.ModelAdmin):
    fields = ('uri', 'name', 'first_name', 'last_name', 'authority')
    readonly_fields = ('uri', 'name', 'first_name', 'last_name')
    search_fields = ('last_name', 'first_name')
    inlines = (AttendanceInline,
               AffiliationInline,
               InvestigatorInline,
               LocalizationInline)


class InstitutionAdmin(admin.ModelAdmin):
    fields = ('uri', 'name', 'authority')
    readonly_fields = ('uri', 'name')
    inlines = (AffiliationInline, )


class CourseGroupAdmin(admin.ModelAdmin):
    fields = ('uri', 'name')
    readonly_fields = ('uri', 'name')
    inlines = (PartOfInline, )


class CourseAdmin(admin.ModelAdmin):
    fields = ('uri', 'name')
    readonly_fields = ('uri', 'name')
    inlines = (PartOfInline, AttendanceInline)


class LocationAdmin(admin.ModelAdmin):
    fields = ('uri', 'name', 'authority')
    readonly_fields = ('uri', 'name')
    inlines = (LocalizationInline, )


class AffiliationAdmin(admin.ModelAdmin):
    fields = ('year', 'person', 'institution', 'position')
    readonly_fields = ('year', 'person', 'institution', 'position')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class AttendanceAdmin(admin.ModelAdmin):
    fields = ('year', 'person', 'course', 'role')
    readonly_fields = ('year', 'person', 'course', 'role')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class InvestigatorAdmin(admin.ModelAdmin):
    fields = ('year', 'person', 'subject', 'role')
    readonly_fields = ('year', 'person', 'subject', 'role')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class PartOfAdmin(admin.ModelAdmin):
    fields = ('year', 'course', 'coursegroup')
    readonly_fields = ('year', 'course', 'coursegroup')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}



class LocalizationAdmin(admin.ModelAdmin):
    fields = ('year', 'person', 'location')
    readonly_fields = ('year', 'person', 'location')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}



# Register your models here.
admin.site.register(Person, PersonAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(PartOf, PartOfAdmin)
admin.site.register(Localization, LocalizationAdmin)
admin.site.register(Investigator, InvestigatorAdmin)
admin.site.register(KnownLocation)
admin.site.register(KnownPerson)
admin.site.register(KnownInstitution)
