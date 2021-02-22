from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils .translation import ugettext as _
from django.contrib.auth import password_validation

class UCF(UserCreationForm):
    email = forms.EmailField(label=_("Correo electrónico"))
    first_name = forms.CharField(label=_("Nombres"))
    last_name = forms.CharField(label=_("Apellidos"))
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_(password_validation.password_validators_help_text_html()),
    )
    password2 = forms.CharField(
        label=_("Confimación de contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Escriba la misma contraseña de antes."),
    )
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email"
        ]