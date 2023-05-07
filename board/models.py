# Create your models here.
from django.db import models


class Question(models.Model):
    topic = models.CharField(max_length=400, default='')
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    email = models.EmailField(max_length=400)
    question_key = models.CharField(max_length=200)
    is_answer = models.IntegerField(default=0)
    ip = models.CharField(max_length=400, default='')
    user_agent = models.CharField(max_length=400, default='')
    create_time = models.CharField(max_length=100,default='')

    class Meta:
        ordering = ['-id']

class BoardIfo(models.Model):
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    visitis = models.IntegerField()
    count = models.IntegerField()
