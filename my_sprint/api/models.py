from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level_winter = models.CharField(max_length=10, blank=True, null=True)
    level_summer = models.CharField(max_length=10)
    level_autumn = models.CharField(max_length=10)
    level_spring = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, default='new')

class PerevalImage(models.Model):
    pass_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    img = models.TextField()  # Assuming base64 encoded image data
    title = models.CharField(max_length=255)
