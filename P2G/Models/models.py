from django.db import models

class Score(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    score = models.IntegerField(default=0, null=False)

    date = models.DateField()

def __str__(self):

    return self.id

class Game(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=64, unique=True)

    link = models.URLField(null=False)

    play_count = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

def __str__(self):

    return self.name

class Categories(models.Model):

    name = models.CharField(max_length=64, unique=True)

    likes = models.IntegerField(default=0)

def __str__(self):

    return self.name

class User(models.Model):

    games = models.ManyToManyField(Game, on_delete=models.CASCADE)

    groups = models.ManyToManyField(Group, on_delete=models.CASCADE)

    friends = models.ManyToManyField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=64, unique=True)

    email = models.CharField(max_length=64)

    profile_image = models.URLField()

    bio = models.CharField(max_length=512)

def __str__(self):

    return self.name

class Group(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    name = models.CharField(max_length=64, null=False)

def __str__(self):

    return self.id