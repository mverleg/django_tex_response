from django.urls import path

from gen.api import generate_latex_file

urlpatterns = [
    path('', generate_latex_file),
]
