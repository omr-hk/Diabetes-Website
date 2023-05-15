from django.db import models

# Create your models here.

class Patient(models.Model):
    gender=models.CharField(max_length=6)
    age=models.PositiveIntegerField()
    hypertension=models.IntegerField()
    heart_disease=models.IntegerField()
    smoking_history=models.CharField(max_length=11)
    bmi=models.FloatField()
    HbA1c_level=models.FloatField()
    blood_glucose_level=models.IntegerField()
    diabetes=models.IntegerField()