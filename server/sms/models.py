from django.db import models

# Create your models here.
class Headline(models.Model):
    link_one = CharField(max_length=200)
    link_two = CharField(max_length=200)
    link_three = CharField(max_length=200)
    link_four = CharField(max_length=200)
    link_five = CharField(max_length=200)
