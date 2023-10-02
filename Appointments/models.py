from django.db import models
from jsonfield import JSONField
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Doctors(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default = uuid.uuid4)
    name = models.CharField(max_length=200)
    speciality = models.CharField(max_length = 300)
    location = models.CharField(max_length=255,default = "Delhi",editable=False)
    rating = models.IntegerField(default = 1,validators=[MinValueValidator(1), MaxValueValidator(5)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)
    schedule_options = (('Monday','Monday'),
                        ('Tuesday','Tuesday'),
                        ('Wednesday','Wednesday'),
                        ('Thursday','Thursday'),
                        ('Friday','Friday'),
                        ('Saturday','Saturday'),
                        )
    weekly_schedule= models.CharField(max_length=10,choices = schedule_options,default = 'Monday')

    appointment_choices = []
    for hour in range(17,21):
        for minute in range(0,60,30):
            time_str = f"{hour:02d}:{minute:02d}"
            appointment_choices.append((time_str,time_str))
    appointment_time = models.CharField(max_length=5,choices=appointment_choices,default='5:00 PM')

    status = models.CharField(max_length=255, default='pending', editable=False)

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.doctor.appointment_time}"