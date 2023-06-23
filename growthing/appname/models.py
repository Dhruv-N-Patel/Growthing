from django.db import models

# Create your models here.
CHOICES = (
    ('programming','Programming'),
    ('design', 'design'),
    ('video editing','Video editing'),
    ('marketing','Marketing'),
    ('misc','Misc'),
)
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    tag = models.CharField(max_length=20, choices=CHOICES, default='misc')
    def __str__(self):
        return self.title
    
class Roadmap(models.Model):
    project_name = models.CharField(max_length=255)
    roadmap = models.TextField()

    def __str__(self):
        return self.project_name

class Meta:
    app_label = 'appname'