from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class MyManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise Http404('No {} matches the given query.'.format(self.model._meta.object_name))
