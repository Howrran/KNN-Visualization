from django import forms

# Test Changes
class CoordinateInputForm(forms.Form):
    x = forms.IntegerField(label='x')
    y = forms.IntegerField(label='y')
    z = forms.IntegerField(label='z')
    clas = forms.IntegerField(label='Class')