from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Passenger(models.Model):
    arabic_name = models.CharField(max_length=150)
    english_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=14, unique=True)
    data_of_birth = models.DateField()
    passport_number = models.CharField(max_length=9, unique=True)
    passport_start = models.DateField()
    passport_end = models.DateField()
    visa_type = models.CharField(max_length=150, default='زيارة شخصية')
    visa_number = models.CharField(max_length=150)
    visa_start = models.DateField()
    visa_end = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, blank=True)

    def get_absolute_url(self):
        return reverse('mysite:passenger_details', args=[self.national_id])

    def __str__(self):
        return self.arabic_name

    class Meta:
        ordering = ['-created']
