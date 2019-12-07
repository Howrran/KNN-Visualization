from django import forms

class CoordinateInputForm(forms.Form):
    x = forms.IntegerField(label='x')
    y = forms.IntegerField(label='y')
    z = forms.IntegerField(label='z')
