from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import datetime


# Create your models here.

class User(AbstractUser):
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=300)
    header_image = models.ImageField(null=True, blank=True, upload_to='profilePic/')
    middle_name = models.CharField(max_length=100, default='')
    date_of_birth = models.DateField(null=True,blank=True)
    contact_no = models.CharField(max_length=16)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=10,default='None')

    def calculateAge(self):
        today = datetime.date.today()
        try:
            birthday = self.date_of_birth.replace(year=today.year)

        # raised when birth date is February 29
        # and the current year is not a leap year
        except ValueError:
            birthday = self.date_of_birth.replace(year=today.year,
                                    month=self.date_of_birth.month + 1, day=1)

        if birthday > today:
            return today.year - self.date_of_birth.year - 1
        else:
            return today.year - self.date_of_birth.year


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.first_name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    doctor_reg_id = models.CharField(max_length=100,default="-")
    specialization = models.CharField(max_length=100)
    fees = models.IntegerField(max_length=6,default=0)
    experience = models.IntegerField(max_length=2,default=0)
    degrees = models.CharField(max_length=250,default="No degrees Specified")
    degree_certificate = models.FileField(null=True, blank=True, upload_to='degreeCertificate/')
    bio = models.TextField(default="-")
    likes = models.ManyToManyField(Patient, related_name="doctor_likes")
    dislikes = models.ManyToManyField(Patient, related_name="doctor_dislikes")
    chamber_address = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor_reg_id'], name='unique_doctor_reg_id')
        ]

    def __str__(self):
        return self.user.first_name

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.first_name
