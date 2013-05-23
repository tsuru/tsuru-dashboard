from django.db import models


class Intro(models.Model):
    email = models.EmailField()
