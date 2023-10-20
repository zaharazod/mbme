
from django.forms import Form, ModelChoiceField
from django.forms.fields import MultiValueField, CharField
from .models import Kingdom, Phylum, Order, Klass, Genus, Species, Animal


class TaxonomyField(MultiValueField):

    def __init__(self, queryset, *args, **kwargs):

        fields = (
            ModelChoiceField(
                queryset=queryset,
                to_field_name='name'
            ),
            CharField(
                validators=[],
                required=False
            )
        )
        kwargs.update({
            'fields': fields,
            'label': queryset.model._meta.model_name,
            'required': False,
            'require_all_fields': False,
        })
        super().__init__(*args, **kwargs)


# class TaxonomyField(ModelChoiceField):
#     def __init__(self, *args, **kwargs):

#         super().__init__(blank=True, *args, **kwargs)


class TaxonomyForm(Form):
    template_name = 'biology/taxonomy_form.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        taxes = (Kingdom, Phylum, Order, Klass, Genus, Species, Animal)
        parent = None
        for tax in taxes:
            field_name = f'tax_{tax._meta.model_name}'
            queryset = tax.objects.all()
            if parent:
                pass
            select = ModelChoiceField(
                queryset=queryset,
                to_field_name='name',
                required=False)
            create = CharField(max_length=50,
                               required=False,
                               empty_value='create..')
            self.fields[f'{field_name}_sel'] = select
            self.fields[f'{field_name}_new'] = create
            parent = tax
