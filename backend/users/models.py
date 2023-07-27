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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = [['author', 'user']]

    def __str__(self) -> str:
        return f'{self.author}'
