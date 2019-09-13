import time

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse

from gen.form import LatexToPdfRequest
from gen.latex import render_pdf_binary
from tex_response import LatexException


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
    form = LatexToPdfRequest(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest('{}\n{}\n'.format('\n'.join(form.errors.values()), form.non_field_errors()))
    key = form.cleaned_data['key']
    if settings.ACCESS_KEY != key:
        return HttpResponse("the provided post 'key' was incorrect\n", status=401)
    # if not request.FILES or 'latex' not in request.FILES:
    #     return HttpResponseBadRequest("request should contain 'latex' as post data\n")
    latex_file = form.cleaned_data['latex']
    latex = latex_file.file.read()
    try:
        #TODO @mark: this still does a djanog render, but I have no context - rather just render directly
        pdf = render_pdf_binary(latex, {})
    except LatexException as ex:
        return HttpResponseBadRequest(ex.message)
    name = '{}_{}.pdf'.format(time.time(), Counter.next())
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="\'{}\'"'.format(name)
    return response

