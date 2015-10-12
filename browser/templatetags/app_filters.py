from django.template import Library

register = Library()


@register.filter(name="get_range")
def get_range(value, offset=0):
    return range(offset, value+offset)


@register.filter
def get_years(coursegroup):
    years = [ p.year for p in coursegroup.partof_set.all()]
    if min(years) == max(years):
        return u'{year}'.format(year=min(years))
    return u'{min} to {max}'.format(min=min(years), max=max(years))


@register.filter
def get_attendance(course):
    """
    Retrieve :class:`.Attendance` instances associated with ``course``.

    Results are ordered by role.
    """
    return course.attendance_set.distinct('role', 'person_id').order_by('role', 'person_id')


@register.filter
def get_affiliation(person, year):
    return person.affiliation_set.filter(year=year).distinct('institution_id')


@register.filter
def get_location(person, year):
    return person.localization_set.filter(year=year).distinct()


@register.filter
def get_affiliation_count(course):
    attendances = get_attendance(course)
    affiliations = [aff for att in attendances
                    for aff in get_affiliation(att.person, att.year)]
    return len(affiliations)

@register.filter
def get_coursegroup_attendance_count(coursegroup):
    return sum([get_attendance(course).count() for course in coursegroup.courses.all()])


@register.filter
def get_partof_set(coursegroup):
    return coursegroup.partof_set.distinct('year', 'course_id').order_by('year', 'course_id')
