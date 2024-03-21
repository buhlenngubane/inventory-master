from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext


def handler404(request, exception, template_name="error_pages/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    template_name="error_pages/500.html"
    response = render(template_name)
    response.status_code = 500
    return response

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "img" / "favicon.ico").open("rb")
    return FileResponse(file)