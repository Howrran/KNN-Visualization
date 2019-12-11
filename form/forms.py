from django import forms

# Test Changes
class CoordinateInputForm(forms.Form):
    x = forms.FloatField(label='x')
    y = forms.FloatField(label='y')
    z = forms.FloatField(label='z')
    clas = forms.IntegerField(label='Class', min_value=1, max_value=10, required=False)
    k = forms.IntegerField(label='set new K', min_value=0, required=False, max_value=999)
    show_lines = forms.BooleanField(label='Show Lines ', required=False)

