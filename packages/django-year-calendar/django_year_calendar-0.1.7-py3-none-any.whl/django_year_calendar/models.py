from django.contrib.contenttypes.models import ContentType
from django.db import models

class EventMixin:
    def ctype_id(self):
        cls = self._meta.model
        ct = ContentType.objects.get_for_model(cls)
        return ct.pk

    def cls_label(self):
        return self._meta.verbose_name
