from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .validators import username_value_not_me

ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator, username_value_not_me],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email'),
        blank=False,
        unique=True,
        max_length=254,
        error_messages={
            "unique": _('A user with that email already exists.'),
        },
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
    )
    role = models.TextField(
        _('role'),
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.TextField(
        'confirmation code',
        blank=True
    )
