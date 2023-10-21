from django.contrib import admin
from .models import Kingdom, Phylum, Order, Klass, Genus, Species, Animal

admin.site.register((Kingdom, Phylum, Order, Klass, Genus, Species, Animal),)
