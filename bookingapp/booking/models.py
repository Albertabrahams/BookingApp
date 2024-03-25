from django.db import models

class Booking(models.Model):
    room = models.ManyToManyField('room.Room', related_name='bookings')
    trin = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    attendees = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.attendees} people"
