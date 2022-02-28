from django.db import models
import datetime

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(default=None)
    sign_up_date = models.DateTimeField('date registered')

    class Meta:
        db_table = 'user'

class Post(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

    class Meta:
        db_table = 'post'

