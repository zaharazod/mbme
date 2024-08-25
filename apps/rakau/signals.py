from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ContentMixin


@receiver(post_save, ContentMixin)
def handle_context_node(sender, **kwargs):
    nodes = sender.nodes
    print(nodes)
