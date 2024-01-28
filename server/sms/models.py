from django.db import models

# Create your models here.
class Headline(models.Model):
    link_one = models.CharField(max_length=200)
    link_two = models.CharField(max_length=200)
    link_three = models.CharField(max_length=200)
    link_four = models.CharField(max_length=200)
    link_five = models.CharField(max_length=200)
