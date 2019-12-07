from django.shortcuts import render
from django.views import View

class FormView(View):

    def get(self, request):
        return render(request, 'form.html', {})