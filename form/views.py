from django.shortcuts import render
from django.views import View
from .forms import CoordinateInputForm
from .knn import Knn

class FormView(View):

    def get(self, request):
        form = CoordinateInputForm()
        return render(request, 'form.html', {'form' : form})

    def post(self, request):
        form = CoordinateInputForm(request.POST)

        knn = Knn(3)

        if form.is_valid():
            context = form.cleaned_data
            x = context['x']
            y = context['y']
            z = context['z']
            clas = context['clas']

            if clas == None:
                knn.add_new_point(x, y, z)
            else:
                knn.add_known_point(x, y, z, clas)

            knn.plot_with_lines()

            return render(request, 'form.html', {'context': context, 'form': form})
        else:
            return render(request, 'error.html', form.errors)