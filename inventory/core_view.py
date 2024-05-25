from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext


def handler404(request, exception):
    print(request)
    print('Hello')
    return render(request, "error_pages/404.html", {})


def handler500(request, *args, **argv):
    return render(request, "error_pages/500.html", {})

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = open(settings.BASE_DIR +"/static/img/favicon.ico","rb")
    return FileResponse(file)