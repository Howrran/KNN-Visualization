from django.shortcuts import render
from django.views import View
from .forms import CoordinateInputForm
from .knn import Knn

class FormView(View):
    knn = Knn(3)

    def get(self, request):
        form = CoordinateInputForm()
        self.knn.reset()

        return render(request, 'form.html', {'form' : form})

    def post(self, request):
        form = CoordinateInputForm(request.POST)



        if form.is_valid():
            context = form.cleaned_data
            x = context['x']
            y = context['y']
            z = context['z']
            clas = context['clas']
            show_lines = context['show_lines']

            if self.knn.is_classes_empty() and clas == None:
                return render(request, 'empty_class_error.html', form.errors)


            if context['k'] != None:
                self.knn.set_k(context['k'])

            if clas == None:
                self.knn.add_new_point(x, y, z)
            else:
                self.knn.add_known_point(x, y, z, clas)

            if show_lines:
                self.knn.plot_with_lines()
            else:
                self.knn.plot()

            return render(request, 'form.html', {'context': context, 'form': form})
        else:
            return render(request, 'error.html', form.errors)