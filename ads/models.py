from django.core.validators import MinLengthValidator
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey('users.User', related_name="ad", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="pictures")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=10, unique=True, validators=[MinLengthValidator(5)], null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self):
        return self.name