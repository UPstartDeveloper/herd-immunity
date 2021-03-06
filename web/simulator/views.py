from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, ModelFormMixin
from simulator.models import Experiment, TimeStep
from simulator.forms import ExperimentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


class ExperimentCreate(CreateView):
    '''User is able to make a new experiment on the system.'''
    model = Experiment
    form_class = ExperimentForm
    template_name = 'simulator/create.html'

    def form_valid(self, form, *args, **kwargs):
        '''Adds model instances to the db as appropriate.'''
        self.object = form.save()
        self.object.run_experiment()
        return HttpResponseRedirect(self.get_success_url())


class ExperimentDetail(DetailView):
    '''Displays a page with results of a specific experiment.'''
    model = Experiment
    template_name = 'simulator/results.html'

    def get(self, request, pk):
        """Renders a page to show the information related to a single
           Experiment.

           Parameters:
           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance

           Returns:
           HttpResponse: the view of the detail template

        """
        experiment = self.get_queryset().get(pk=pk)
        time_steps = TimeStep.objects.filter(experiment=experiment)
        context = {
            'experiment': experiment,
            'time_steps': time_steps
        }
        return render(request, self.template_name, context)


class ExperimentList(ListView):
    '''List all the Experiments that have been conducted by users.'''
    model = Experiment
    template_name = 'simulator/list.html'

    def get(self, request):
        """Get a list of all Experiment instances. """
        experiments = self.get_queryset().all()
        return render(request, self.template_name, {
          'experiments': experiments
        })


def show_landing(request):
    '''Render the landing page of the website.'''
    return render(request, 'simulator/index.html')


def show_about_page(request):
    '''Render the About page of the site, so users can get more info.'''
    return render(request, 'simulator/info.html')


class InfectedNodeDetail(DetailView):
    '''Displays a page with population tree of an Experiment.'''
    model = Experiment
    template_name = 'simulator/spread-of-disease.html'

    def get(self, request, pk):
        """Renders a page to show the spread of disease, using an M-way tree.

           Parameters:
           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance

           Returns:
           HttpResponse: the view of the detail template

        """
        experiment = self.get_queryset().get(pk=pk)
        context = {'experiment': experiment}
        return render(request, self.template_name, context)
