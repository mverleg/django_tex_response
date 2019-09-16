import time

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse

from gen.form import LatexToPdfRequest
from tex_response import LatexException
from tex_response.tex import tex_str_to_pdf_bytes


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
        pdf = tex_str_to_pdf_bytes(latex, tex_cmd='xelatex')
    except LatexException as ex:
        return HttpResponse(ex.message, status=400)
    name = '{}_{}.pdf'.format(time.time(), Counter.next())
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="\'{}\'"'.format(name)
    return response

