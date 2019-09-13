from django import forms


class LatexToPdfRequest(forms.Form):
    key = forms.CharField(max_length=128)
    latex = forms.FileField(allow_empty_file=False)

