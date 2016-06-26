from django.conf import settings


def git_revision(request):
    return {'git_revision': settings.GIT_REVISION}
