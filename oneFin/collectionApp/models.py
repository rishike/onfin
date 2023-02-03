from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import uuid

# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="user", on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Movies(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.CharField(max_length=200,null= True, blank= True)
    uuid = models.CharField(max_length=250)
    collection = models.ForeignKey(Collection, related_name="movies", on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)