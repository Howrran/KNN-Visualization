from django.shortcuts import render
from django.views import View
from .forms import CoordinateInputForm

class FormView(View):

    def get(self, request):
        form = CoordinateInputForm()
        return render(request, 'form.html', {'form' : form})

    def post(self, request):
        form = CoordinateInputForm(request.POST)

        if form.is_valid():
            context = form.cleaned_data

            return render(request, 'form.html', context)
        else:
            return render(request, 'error.html', form.errors)