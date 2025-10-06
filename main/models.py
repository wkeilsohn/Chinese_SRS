from django.db import models

# Create your models here.

class User_Words(models.Model):
    user_name = models.CharField(max_length=50)
    word = models.CharField(max_length=10)
    meaning = models.CharField(max_length=100)
    sheet_level = models.IntegerField(default=1)
    last_studied = models.DateTimeField()
    study_level = models.CharField(max_length=2)
    word_level = models.IntegerField(default=1)
    incorect_times = models.IntegerField(default=0)

class Hanzi(models.Model):
    word = models.CharField(max_length=10)
    traditional_word = models.CharField(max_length=10)
    meaning = models.CharField(max_length=100)
    sheet_level = models.IntegerField(default=1)

