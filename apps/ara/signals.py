from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ContextMixin


@receiver(post_save, ContextMixin)
def handle_context_node(sender, **kwargs):
    nodes = sender.nodes
    print(nodes)
