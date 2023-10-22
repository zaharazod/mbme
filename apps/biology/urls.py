from django.urls import path
from .views import TaxonomyEditView
app_name = 'biology'
urlpatterns = [
    # path('', lambda, name='index'),
    path('edit/', TaxonomyEditView.as_view(), name='taxonomy-edit'),
]
