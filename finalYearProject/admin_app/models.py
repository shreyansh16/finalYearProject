from django.db import models
from django.urls import reverse

# Create your models here.
class Specialization(models.Model):
    header_image = models.ImageField(null=True, blank=True, upload_to="imagesSpl/")
    category = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.category



class BannedUser(models.Model):
    userid = models.CharField(max_length=1000,primary_key=True)

    def __str__(self):
        return self.userid


