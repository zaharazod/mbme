from django.template import Library
from vaticinator.vaticinator import Vaticinator

register = Library()
vaticinator = Vaticinator()

@register.simple_tag
def random_fortune(*args, **kwargs):
    vaticinator.set_default_options()
    vaticinator.process_options(*args, **kwargs)
    return vaticinator.fortune
