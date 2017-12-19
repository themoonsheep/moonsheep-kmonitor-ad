from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from moonsheep.views import TaskView as MTaskView
from .models import Politician


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            # TODO
            'reporting_year': 'reporting_year',
            'stats_counted_from': '2015',
            'stats': {
                'volunteers_count': 0,
                'time_spent_hours': 0,
                'liberated_declarations_since_iceage': 996,
                'liberated_declarations': 123,
                'all_declarations_count': 187
            }
        })
        return context


class TaskIntroView(TemplateView):
    template_name = 'task_intro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            # TODO
            'mp': {
                'name': 'Brominator',
                'image_url': 'https://vignette.wikia.nocookie.net/broforce/images/7/74/Brominator_face.png/revision/latest?cb=20150705030550',
                'party': {
                    'name': 'Broforce'
                }
            },
            'task': {
                'id': 0  # TODO preshow task
            }
        })
        return context


class TaskView(MTaskView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mp': Politician.objects.get_or_none(id=self.task.data['politician_id']),
        })
        return context

    def get_success_url(self):
        return reverse('task')
