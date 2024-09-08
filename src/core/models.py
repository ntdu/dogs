import uuid
from os.path import splitext

from django.db import models


class Bread(models.Model):
    weight = models.JSONField()
    height = models.JSONField()
    external_id = models.CharField(max_length=4)
    name = models.CharField(max_length=150)
    bred_for = models.CharField(max_length=255)
    breed_group = models.CharField(max_length=255)
    life_span = models.CharField(max_length=255)
    temperament = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    reference_image_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.external_id} | {self.name}"


class Image(models.Model):
    def upload_image_to(instance, filename):
        _, extension = splitext(filename)
        return f"{uuid.uuid4().hex}{extension}"

    bread = models.ForeignKey(Bread, null=True, blank=True, on_delete=models.CASCADE, related_name="images")

    name = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(blank=True, null=True, upload_to=upload_image_to)
    type = models.CharField(max_length=255, null=True, blank=True)
    size = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.bread.name} | {self.name}"
