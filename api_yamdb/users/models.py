import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    first_name = models.CharField(
        max_length=40,
        verbose_name='Имя',
        unique=False,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name='Фамилия',
        unique=False,
        blank=True,
        null=True
    )

    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=150,
                                unique=True,
                                validators=[
                                    RegexValidator(
                                        regex='[^/w]+',
                                        message='Введен неверный формат')]
                                )

    email = models.EmailField(verbose_name='Адрес электронной почты',
                              unique=True)

    bio = models.CharField(max_length=100,
                           verbose_name='О себе',
                           blank=True,
                           null=True,)

    role = models.CharField(verbose_name='Роль',
                            max_length=50,
                            choices=ROLE_CHOICES,
                            blank=True,
                            null=True,
                            default=USER
                            )

    confirmation_code = models.CharField(max_length=256, default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
