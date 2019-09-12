import time

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST


class Counter:
    value = 0

    @classmethod
    def next(cls):
        cls.value += 1
        return cls.value


@require_POST
def generate_latex_file(request):
    if 'key' not in request.POST:
        return HttpResponseForbidden("request should contain 'key' as post data\n")
    key = request.POST['key']
    if settings.ACCESS_KEY != key:
        return HttpResponseForbidden("the provided post 'key' was incorrect\n")
    if 'latex' not in request.POST:
        return HttpResponseBadRequest("request should contain 'latex' as post data\n")
    latex = request.POST['latex']
    pdf = b''
    name = '{}_{}.pdf'.format(time.time(), Counter.next())
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="\'{}\'"'.format(name)
    return response

