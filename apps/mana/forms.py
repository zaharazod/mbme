from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ManaUser


class ManaUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ManaUser


class ManaUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = ManaUser
