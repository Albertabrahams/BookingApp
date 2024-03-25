from django.db import models

class Room(models.Model):
    size = models.IntegerField()
    view = models.CharField(max_length=50, choices=[
        ('sea', 'Sea Side'),
        ('forest', 'Forest Side'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.view} - {self.size} people"
