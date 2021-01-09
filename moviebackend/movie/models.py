from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    user_md5 = models.CharField(primary_key=True, max_length=255)
    updatetime = models.IntegerField()#验证token时间
    password = models.CharField(null=True,max_length=255)
    token = models.CharField(max_length=32)
    user_nickname = models.CharField(null=True,max_length=50)


    def __str__(self):
        return self.user_md5

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Movie(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
    name = models.CharField(null=True, max_length=255)
    alias = models.CharField(null=True, max_length=255)
    actors = models.CharField(null=True, max_length=255)
    cover = models.CharField(null=True, max_length=50)
    directors = models.CharField(null=True, max_length=255)
    score = models.FloatField(null=True)
    votes = models.IntegerField(null=True)
    genres = models.CharField(null=True, max_length=255)
    languages = models.CharField(null=True, max_length=255)
    mins = models.IntegerField(null=True)
    official_site = models.CharField(null=True, max_length=255)
    regions = models.CharField(null=True,max_length=255)
    release_date = models.CharField(null=True,max_length=55)
    slug = models.CharField(null=True, max_length=50)
    storyline = models.TextField(null=True)
    tags = models.CharField(null=True, max_length=255)
    year = models.IntegerField(null=True)
    actor_ids = models.CharField(null=True, max_length=255)
    director_ids = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.movie_id

    class Meta:
        verbose_name = '电影'
        verbose_name_plural = '电影'



class rating(models.Model):
    rating_id = models.BigAutoField(primary_key=True)
    movie_id = models.BigIntegerField(null=True)
    rating = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    user_md5 = models.CharField(null=True,max_length=255)
    def __str__(self):
        return self.rating_id