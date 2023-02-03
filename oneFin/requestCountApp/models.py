from django.db import models

# Create your models here.
class RequestCounter(models.Model):
    request_count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.request_count)