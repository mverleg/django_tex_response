
Django Tex Response
-----------

Very simple code that lets you use your installed TeX compiler to render a .tex template to a pdf-file response. You can use anything from the Django template language in your TeX file, just escape (rare) TeX construct that have meaning to Django (e.g. {{ ).

Installation & Configuration:
-----------

- Install using ``pip install git+https://bitbucket.org/mverleg/django_tex_response.git``
- Import using ``from tex_response import render_pdf``

Alternatively you can download just the tex.py file and put it in your project; this contains everything.

How to use it
-----------

- Put your .tex file somewhere that the Django template engine can find.
- Escape anything in your TeX code that has special meaning for Django, such as {{ or {% constructs. This can be done with {% templatetag openbrace %} etc, see https://docs.djangoproject.com/en/dev/ref/templates/builtins/#templatetag
- Optionally add Django template commands, like variables (``{{ date }}``) or even loops.
- Your view would look something like this:

                return render_pdf(request, 'textest.tex', {'date': datetime.now()}, filename = 'testfile.pdf')

What else?
-----------

There isn't much to this, it's really simple. However, you can also import and use:

- render_tex : renders the template to a .tex file without compiling the pdf (returns the temporary file path)
- tex_to_pdf : given a .tex file, compiles the .pdf result (deletes the .tex file) (returns the temporary file path)
- LatexException : catch this in case of problems

It doesn't work
-----------



If your tex file compiles fine outside Django, you can make sure that Django uses the same command by providing these arguments:

- tex_cmd (default 'lualatex')
- flags (default ['-interaction=nonstopmode', '-halt-on-error'])

Django Tex Response has been tested on Ubuntu with texlive-full. Fixes for other platforms are most welcome.

How it does it's thing
-----------

Django Tex Response is very simple. It:

1. renders the .tex file using Django, as if it were a normal template
2. writes the result to a temporary directory
3. uses Popen to run your tex installation (default 'lualatex') to compile it
4. turns the output pdf into a response
5. deletes temporary files

License
-----------

django_tex_response is available under the revised BSD license, see LICENSE.txt. You can do anything as long as you include the license, don't use my name for promotion and are aware that there is no warranty.


