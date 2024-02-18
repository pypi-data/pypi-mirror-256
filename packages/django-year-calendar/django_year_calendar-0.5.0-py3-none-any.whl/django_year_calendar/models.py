from django.contrib.contenttypes.models import ContentType
from django.db import models

class EventMixin:
    border_level = 0
    force_color = None
    def ctype_id(self):
        cls = self._meta.model
        ct = ContentType.objects.get_for_model(cls)
        return ct.pk

    def cls_label(self):
        return self._meta.verbose_name

    def cls_template_name(self):
        return './%s.html' % self._meta.model_name
