from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from users.validators import check_birth_date, check_email_address


# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.name


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')
    ADMIN = 'admin', _('admin')


class User(AbstractUser):
    role = models.CharField(max_length=9, choices=UserRoles.choices)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    locations = models.ManyToManyField(Location)
    birth_data = models.DateField(verbose_name="Дата рождения", validators=[check_birth_date], null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True, validators=[check_email_address])
    # email = models.EmailField(unique=True, blank=True, null=True,
    #                           validators=[RegexValidator(regex="@rambler.ru",
    #                                                      inverse_match=True,
    #                                                      message="регистрация с домена rambler.ru запрещена.")])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save(*args, **kwargs)

# class User(models.Model):
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200, null=True, blank=True)
#     username = models.CharField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)
#     role = models.CharField(max_length=9, choices=UserRoles.choices)
#     age = models.PositiveSmallIntegerField()
#     locations = models.ManyToManyField(Location)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return self.username