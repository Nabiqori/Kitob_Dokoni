from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Account(AbstractUser):
    image = models.ImageField(upload_to='accounts/', blank=True, null=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.CharField(max_length=50, null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Image(models.Model):
    image = models.ImageField(upload_to='books/')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

class Wishlist(models.Model):
    books = models.ManyToManyField(Book)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username
