from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator

from .validators import validator_username


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):

    role = models.TextField(max_length=30,
                            choices=UserRole.choices,
                            default=UserRole.USER,
                            verbose_name='Роль')
    bio = models.TextField('Биография', null=False, blank=True)
    confirmation_code = models.TextField(blank=True, null=True)
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
    )
    username = models.CharField(unique=True,
                                max_length=150,
                                validators=[ASCIIUsernameValidator(),
                                            validator_username, ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.is_superuser
                or self.role == UserRole.ADMIN
                or self.is_staff)

    @property
    def is_moder(self):
        return self.role == UserRole.MODERATOR
