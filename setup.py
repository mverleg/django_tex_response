# -*- coding: utf-8 -*-

'''
    for installing with pip
'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='tex_response',
    version='1.0.0',
    author=u'Mark V',
    author_email='noreply.mail.nl',
    packages=find_packages(),
    include_package_data=True,
    url='git+https://bitbucket.org/mverleg/django_tex_response.git',
    license='revised BSD license; see LICENSE.txt',
    description='Very simple code that lets you use your installed TeX compiler to render a .tex template to a pdf-file response.',
    zip_safe=True,
    install_requires = [],
)
