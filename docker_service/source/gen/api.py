import time

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse

from docker_service.source.gen.form import LatexToPdfRequest
from docker_service.source.gen.latex import render_pdf_binary


class Counter:
    value = 0

    @classmethod
    def next(cls):
        cls.value += 1
        return cls.value


def generate_latex_file(request):
    if request.method == 'GET':
        return HttpResponse("Send a post request containing 'key' and 'latex'\nExample request:\ncurl -X POST "
            "localhost:8000 -F \"key=A54eAg@lpPZ94vBzI%7Qd0RC_P0wQR6$\" "
            "-F \"latex=@/home/mark/latex_example.tex\"\n", status=405)
    if request.method != 'POST':
        return HttpResponse("Send a post request containing 'key' and 'latex'\n", status=405)
    if not request.FILES:
        return HttpResponse("use 'enctype=\"multipart/form-data\"'\n", status=405)

    forms = LatexToPdfRequest(request.POST, request.FILES)
    if not forms.is_valid():
        pass
    #TODO @mark: 

    if 'key' not in request.POST:
        return HttpResponseForbidden("request should contain 'key' as post data\n")
    key = request.POST.get('key', None)
    if settings.ACCESS_KEY != key:
        return HttpResponseForbidden("the provided post 'key' was incorrect\n")
    if not request.FILES or 'latex' not in request.FILES:
        return HttpResponseBadRequest("request should contain 'latex' as post data\n")
    latex = request.FILES.get('latex', None)
    pdf = render_pdf_binary(latex, {})
    name = '{}_{}.pdf'.format(time.time(), Counter.next())
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="\'{}\'"'.format(name)
    return response

