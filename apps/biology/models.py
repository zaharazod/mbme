from django.db import models


class Taxonomy(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Kingdom(Taxonomy):
    pass


class Phylum(Taxonomy):
    kingdom = models.ForeignKey(Kingdom, related_name='phylum',
                                on_delete=models.CASCADE)


class Klass(Taxonomy):
    phylum = models.ForeignKey(Kingdom, related_name='klass',
                               on_delete=models.CASCADE)


class Order(Taxonomy):
    klass = models.ForeignKey(Klass, related_name='order',
                              on_delete=models.CASCADE)


class Family(Taxonomy):
    order = models.ForeignKey(Order, related_name='family',
                              on_delete=models.CASCADE)


class Genus(Taxonomy):
    family = models.ForeignKey(Family, related_name='genus',
                               on_delete=models.CASCADE)


class Species(Taxonomy):
    genus = models.ForeignKey(Genus, related_name='species',
                              on_delete=models.CASCADE)


class Animal(models.Model):
    name = models.CharField(max_length=50, blank=True, default='')
    species = models.ForeignKey(Species, related_name='animals',
                                on_delete=models.CASCADE)
    arrival = models.DateField(blank=True, null=True)
    departure = models.DateField(blank=True, null=True)
