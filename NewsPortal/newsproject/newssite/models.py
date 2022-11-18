from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):

    category_name = models.CharField(max_length=255, unique=True)
    usersubscribtions = models.ManyToManyField(User, through='UsersSubscriptions')

    def __str__(self) -> str:
        return f'{self.category_name}'

class UsersSubscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class New(models.Model):

    created = models.DateTimeField(
        auto_now_add=True,
    )

    name = models.CharField(
        max_length=100000,
        unique=True,
    )
    description = models.TextField()


    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='news',
    )

    categories = models.ManyToManyField(Category, through='NewCategory')

    def __str__(self):
        return f'{self.name.title()}: {self.description[:50000]}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])







class Author(models.Model):

    name = models.CharField(max_length=100000, unique=True)

    def __str__(self):
        return self.name.title()

class NewCategory(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
