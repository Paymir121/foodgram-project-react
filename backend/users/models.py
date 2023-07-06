from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator

from .validators import validator_username


class User(AbstractUser):

    bio = models.TextField('Биография', null=False, blank=True)
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
    )
    username = models.CharField(unique=True,
                                max_length=150,
                                validators=[ASCIIUsernameValidator(),
                                            validator_username, ])
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    password = models.CharField(max_length=150,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    def __str__(self):
        return self.username

