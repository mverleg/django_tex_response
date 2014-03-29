
from django.template.loader import render_to_string
from tempfile import mkdtemp, mkstemp
from os import remove
from os.path import join
from subprocess import Popen, PIPE
from shutil import rmtree, copy2
from django.http.response import HttpResponse
from django.template.context import RequestContext


class LatexException(Exception):
    ''' something went wrong while rendering a tex file '''


def tex_to_pdf(tex_input, destination = mkstemp(suffix = '.pdf')[1], tex_cmd = 'lualatex', flags = ['-interaction=nonstopmode', '-halt-on-error']):
    tmp_dir = mkdtemp()
    in_file, out_file = join(tmp_dir, 'input.tex'), join(tmp_dir, 'output.pdf')
    with open(in_file, 'w+') as fh:
        fh.write(tex_input)
    cmd = 'cd %s; %s %s -jobname=output input.tex' % (tmp_dir, tex_cmd, ' '.join(flags))
    proc = Popen(cmd, stdout = PIPE, stderr = PIPE, shell = True)
    outp, err = proc.communicate()
    if err:
        raise LatexException(err)
    try:
        copy2(out_file, destination)
    except IOError:
        raise LatexException('%s produced no error but failed to produce a pdf file; output: %s' % (tex_cmd, outp))
    rmtree(tmp_dir)
    return destination


def render_pdf(request, template, context, filename = 'file.pdf', tex_cmd = 'lualatex', flags = ['-interaction=nonstopmode', '-halt-on-error']):
    tex_input = render_to_string(template, context, RequestContext(request))
    pdf_file = tex_to_pdf(tex_input, tex_cmd = tex_cmd, flags = flags)
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    with open(pdf_file, 'r') as fh:
        response.write(fh.read())
    remove(pdf_file)
    return response


