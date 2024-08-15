from django.db import models
from django.shortcuts import reverse
from django_quill.fields import QuillField

from apps.mana.models import AuditedMixin
from apps.ara.models import ContentMixin


class Folder(AuditedMixin, ContentMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=False)  # FIXME
    # slug should be unique_together with parent context

    def __str__(self): return self.title[0:20]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = Page.slugify(self.title)
        super().save(*a, **kw)

    @property
    def context_path(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("folder", kwargs={"pk": self.pk})


class Page(Folder):
    draft = models.BooleanField(default=True)


class PageSection(AuditedMixin):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='sections')
    title = models.CharField(
        max_length=255,
        blank=True,
        default='')
    content = QuillField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'section'
