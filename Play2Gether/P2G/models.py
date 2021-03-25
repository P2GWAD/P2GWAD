from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=4096, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    link = models.URLField(null=False)
    play_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=4096, null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)
    friends = models.ManyToManyField('self')
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=512)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False)
    randGroup = models.BooleanField(default=False)
    users = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=0)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    date = models.DateTimeField()


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=0)
    score = models.IntegerField(default=0, null=False)
    approved = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return self.id
