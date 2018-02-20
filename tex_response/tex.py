
"""
Copied from https://bitbucket.org/mverleg/django_tex_response/src/a7859552519d7145473951d6ac2109e72067a4b5?at=master
"""

from django.template.loader import render_to_string
from tempfile import mkdtemp, mkstemp
from os import remove
from os.path import join, dirname
from subprocess import Popen, PIPE
from shutil import rmtree, copy2
from django.http.response import HttpResponse


class LatexException(Exception):
	""" something went wrong while rendering a tex file """


def render_tex(request, template, context):
	"""
	Render template to .tex file.
	"""
	tex_input = render_to_string(template, context, request)
	tmp_dir = mkdtemp()
	in_file = join(tmp_dir, 'input.tex')
	with open(in_file, 'w+') as fh:
		fh.write(tex_input)
	return in_file


def tex_to_pdf(tex_file, destination=mkstemp(suffix='.pdf')[1],
		tex_cmd='lualatex', flags=('-interaction=nonstopmode', '-halt-on-error',)):
	"""
	Render .tex file to .pdf.
	"""
	tmp_dir = dirname(tex_file)
	out_file = join(tmp_dir, 'output.pdf')
	cmd = 'cd {dir:s}; {cmd:s} {flags:s} -jobname=output input.tex'.format(
		dir=tmp_dir, cmd=tex_cmd, flags=' '.join(flags))
	proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	outp, err = proc.communicate()
	if b'error occurred' in outp:
		raise LatexException('... {0:}'.format(outp[-800:]))
	if err:
		raise LatexException(err)
	try:
		copy2(out_file, destination)
	except IOError:
		raise LatexException(('{0:s} produced no error but failed to produce a'
			' pdf file; output: {1:s}').format(tex_cmd, outp))
	rmtree(tmp_dir)
	return destination


def render_pdf(request, template, context, filename='file.pdf',
		tex_cmd='lualatex', flags=('-interaction=nonstopmode', '-halt-on-error',)):
	"""
	Render template to pdf-response (by using the above functions).
	"""
	tex_file = render_tex(request, template, context)
	pdf_file = tex_to_pdf(tex_file, tex_cmd=tex_cmd, flags=flags)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="%s"' % filename
	with open(pdf_file, 'rb') as fh:
		response.write(fh.read())
	remove(pdf_file)
	return response

