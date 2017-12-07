from django.shortcuts import render
from django.views.generic import TemplateView
from moonsheep.views import TaskView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
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
        context = super(TaskIntroView, self).get_context_data(**kwargs)
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

