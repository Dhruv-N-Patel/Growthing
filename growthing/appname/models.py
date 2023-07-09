from django.db import models
from django.contrib.auth.models import User

# Create your models here.
genre = (
    ('programming','Programming'),
    ('design', 'design'),
    ('video editing','Video editing'),
    ('marketing','Marketing'),
    ('misc','Misc'),
)
difficulty=(
    ('easy','Easy'),
    ('moderate','Moderate'),
    ('tough','Tough')
)
class Project(models.Model):
    title = models.CharField(max_length=100)
    emoji = models.CharField(max_length=200, null=True)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    tools = models.CharField(max_length=200, null=True)
    genre = models.CharField(max_length=20, choices=genre, default='misc')
    project_id = models.CharField(max_length=100)
    
    # difficulty = models.CharField(max_length=20, choices=difficulty, default='misc')
    def __str__(self):
        return self.title
    
class Roadmap(models.Model):
    title = models.CharField(max_length=100)
    emoji = models.CharField(max_length=200, null=True)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    tools = models.CharField(max_length=200, null=True)
    genre = models.CharField(max_length=20, choices=genre, default='misc')
    difficulty = models.CharField(max_length=20, choices=difficulty, default='misc')
    generate_roadmap = models.TextField()
    project_id = models.CharField(max_length=100)
    task = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Meta:
    app_label = 'appname'