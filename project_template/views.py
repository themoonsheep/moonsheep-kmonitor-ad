from django.shortcuts import render
from moonsheep.views import TaskView


class TranscriptionView(TaskView):
    template_name = 'transcription.html'
