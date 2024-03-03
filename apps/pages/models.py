from django.db import models
from django.shortcuts import reverse
from django_quill.fields import QuillField
from django_currentuser.db.models import CurrentUserField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Page(models.Model):
    title = models.CharField(max_length=255)
    path = models.CharField(max_length=64)
    context_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    context_id = models.PositiveIntegerField()
    context = GenericForeignKey('context_type', 'context_id')
    content = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(related_name='pages')
    modified_by = CurrentUserField(
        related_name='pages_modified', on_update=True)
    
    
    def __str__(self):
        return 'Page: %s' % self.path
    
    def get_absolute_url(self):
        return reverse("page", kwargs={"pk": self.pk})
    
    
    
