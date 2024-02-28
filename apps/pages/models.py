from django.db import models
from django.shortcuts import reverse
from django_quill.fields import QuillField
from django_currentuser.db.models import CurrentUserField


class Page(models.Model):
    title = models.CharField(max_length=255)
    path = models.CharField(max_length=64)
    content = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(related_name='pages')
    modified_by = CurrentUserField(
        related_name='pages_modified', on_update=True)
    
    def get_absolute_url(self):
        return reverse("page", kwargs={"pk": self.pk})
    
