from django.db import models
from account_app.models import Doctor, Patient

# Create your models here.

CHOICES = (('12:00', '12:00'),('13:00', '13:00') , ('14:00', '14:00') , ('15:00', '15:00') ,('16:00', '16:00') ,('17:00', '17:00'), ('18:00', '18:00') )


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=None)
    a_date = models.CharField(max_length=25)
    a_time = models.CharField(choices=CHOICES,max_length=10)
    p_first_name = models.CharField(max_length=100)
    p_middle_name = models.CharField(max_length=100)
    p_last_name = models.CharField(max_length=100)
    p_gender = models.CharField(max_length=10)
    p_contact_no = models.CharField(max_length=10)
    p_email = models.EmailField()
    p_age = models.IntegerField(default=0,blank=False,null=False)
    visit_reason = models.CharField(max_length=50)
    is_cancelled = models.BooleanField(default=False)
    is_marked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['a_date', 'a_time', 'doctor'], name='unique_appointment_key')
        ]

    def __str__(self):
        return self.doctor.user.first_name + ' ' + self.doctor.user.last_name + ' ' + str(self.a_date) + ' ' + str(self.a_time)


class Reviews(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return 'Review for '+ self.doctor.user.first_name+' '+self.doctor.user.last_name



class DocumentUpload(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=120)
    document_name = models.CharField(max_length=120)
    document = models.FileField(null=True, blank=True, upload_to='documentUpload/')

    def __str__(self):
        return self.p_name + " " + self.document_name