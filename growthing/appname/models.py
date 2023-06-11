from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=200)

class Meta:
    app_label = 'appname'