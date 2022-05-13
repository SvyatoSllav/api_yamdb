from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def username_value_not_me(value):
    if value == 'me':
        raise ValidationError(
            _("%(value)s can't be 'me'."),
            params={'value': value},
        )
