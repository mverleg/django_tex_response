from os import remove

from tex_response.tex import render_tex, tex_to_pdf


def store_or_render(template, context):
    tex_file = render_tex(None, template, context)
    pdf_tmp = tex_to_pdf(tex_file, tex_cmd='lualatex',
        flags=('-interaction=nonstopmode', '-halt-on-error',),
        do_link_imgs=True)
    with open(pdf_tmp, 'rb') as fh:
        data = fh.read()
    remove(pdf_tmp)
    return data

