from os import remove
from tempfile import NamedTemporaryFile

from tex_response.tex import render_tex, tex_to_pdf


def render_pdf_binary(latex_bin, context):
    #tex_file = render_tex(None, template, context)
    latex_file = NamedTemporaryFile()
    latex_file.write(latex_bin)
    pdf_tmp = tex_to_pdf(latex_file, tex_cmd='lualatex',
        flags=('-interaction=nonstopmode', '-halt-on-error',),
        do_link_imgs=True)
    with open(pdf_tmp, 'rb') as fh:
        data = fh.read()
    remove(pdf_tmp)
    return data

