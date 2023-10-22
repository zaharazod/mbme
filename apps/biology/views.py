from django.shortcuts import render
from django.views.generic.edit import FormView, ProcessFormView
from django.views.generic.base import ContextMixin, TemplateResponseMixin, TemplateView
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.views import View
from collections import OrderedDict
from .models import Kingdom, Phylum, Order, Klass, Genus, Species, Animal
from .forms import TaxonomyForm


LAYERS = (Kingdom, Phylum, Order, Klass, Genus, Species, Animal)
LAYER_NAMES = [layer.name for layer in LAYERS]

# FormView:
# django.views.generic.base.TemplateResponseMixin
# django.views.generic.edit.BaseFormView
# django.views.generic.edit.FormMixin
# django.views.generic.edit.ProcessFormView
# django.views.generic.base.View


class TaxonomyEditView(FormView):
    template_name = "biology/taxonomy_edit.html"
    form_class = TaxonomyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layers'] = {}
        context['layer_names'] = LAYER_NAMES
        parent = None
        for layer in LAYERS:
            layer_objects = OrderedDict([(row.name, row)
                                         for row in layer.objects.all()])
            context['layers'][layer._meta.model_name] = {
                'parent': parent,
                'objects': layer_objects,
            }
        return context

    # form_class = TaxonomyForm
    success_url = None
    http_method_names = ['get', 'post',]
