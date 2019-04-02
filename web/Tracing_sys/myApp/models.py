from django.db import models

# Create your models here.
class poems(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    poem_body = models.CharField(max_length=1000)
    dynasty = models.CharField(max_length=100)
    tac = models.CharField(max_length=1000)
    appreciation = models.CharField(max_length=1000)
    background = models.CharField(max_length=1000)
    self_intro = models.CharField(max_length=1000)
    def __str__(self):
        return self.title
