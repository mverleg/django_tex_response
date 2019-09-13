from os import remove
from os.path import join
from tempfile import mkdtemp

from tex_response.tex import tex_to_pdf


def render_pdf_binary(latex_bin, context):
    #tex_file = render_tex(None, template, context)
    latex_dir = mkdtemp('latex_gen')
    latex_file = join(latex_dir, 'input.tex')
    with open(latex_file, 'wb+') as fh:
        fh.write(latex_bin)
    pdf_tmp = tex_to_pdf(latex_file, tex_cmd='luatex',
        flags=('-interaction=nonstopmode', '-halt-on-error',),
        do_link_imgs=True)
    with open(pdf_tmp, 'rb') as fh:
        data = fh.read()
    remove(pdf_tmp)
    return data

