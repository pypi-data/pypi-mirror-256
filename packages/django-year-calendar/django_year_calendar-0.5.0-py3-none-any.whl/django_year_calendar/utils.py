import importlib

from django.db import models


def fill_events(params, border_level=0, force_color=None):
    items = list(params['qset']())
    if border_level > 0:
        for ob in items: ob.border_level = border_level
    if force_color:
        for ob in items: ob.force_color = force_color
    return items



def load_manager(view_settings):
    items = view_settings['manager'].split('.')
    if len(items) == 3:
        module, obname = '.'.join(items[:-1]), items[-1]
        module = importlib.import_module(module)
        ob = getattr(module, obname)
        if issubclass(ob, models.Model):
            view_settings['qset'] = ob.objects.all
    elif len(items) == 4:
        module, cls, obname = '.'.join(items[:-2]), items[-2], items[-1]
        module = importlib.import_module(module)
        cls = getattr(module, cls)
        ob = getattr(cls, obname)
        if isinstance(ob, models.Manager):
            view_settings['qset'] = ob.all
    elif len(items) == 5:
        module, cls, obname, method = '.'.join(items[:-3]), items[-3], items[-2], items[-1]
        module = importlib.import_module(module)
        cls = getattr(module, cls)
        ob = getattr(cls, obname)
        fun = getattr(ob, method)
        view_settings['qset'] = fun
def fill_context_extra(kwargs, view_settings):
    kwargs['events'] = []
    if not view_settings: return
    for v in view_settings:
        load_manager(v)
    border_level = 0
    for dic in view_settings:
        if 'qset' in dic:
            force_color = None
            if 'border' in dic and dic['border']: border_level +=1
            if 'force_color' in dic and dic['force_color']: force_color = dic['force_color']
            l = fill_events(dic, border_level, force_color)
            kwargs['events'].extend(l)

