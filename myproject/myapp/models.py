from django.db import models

# Create your models here.
class route(models.Model):
    busname = models.CharField(max_length=100)
    pickplace = models.CharField(max_length=100)
    picktime = models.TimeField()
    destplace =  models.CharField(max_length=100)
    desttime =  models.TimeField()
    contact = models.IntegerField()
    def __str__(self):
        return self.busname


class Gride(models.Model):
    image = models.ImageField(upload_to='images/')
    # def __str__(self):
    #     return self.image

from django.db import models

class message(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/')


class BusBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    date = models.DateField()
    bus_type = models.CharField(max_length=50)
    seats = models.IntegerField()

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='feedback/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} - {self.created_at}"
