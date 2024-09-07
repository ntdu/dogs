from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Bread(models.Model):
    weight = models.JSONField()
    external_id = models.CharField(max_length=4)
    name = models.CharField(max_length=30)
    vetstreet_url = models.URLField(max_length=100)
    temperament = models.CharField(max_length=150)
    origin = models.CharField(max_length=150)
    country_codes = models.CharField(max_length=150)
    country_code = models.CharField(max_length=150)
    description = models.TextField()
    life_span = models.CharField(max_length=150)
    indoor = models.IntegerField()
    alt_names = models.CharField(max_length=150, null=True)
    adaptability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    affection_level = models.IntegerField()
    child_friendly = models.IntegerField()
    dog_friendly = models.IntegerField()
    energy_level = models.IntegerField()
    grooming = models.IntegerField()
    health_issues = models.IntegerField()
    intelligence = models.IntegerField()
    shedding_level = models.IntegerField()
    social_needs = models.IntegerField()
    stranger_friendly = models.IntegerField()
    vocalisation = models.IntegerField()
    experimental = models.IntegerField()
    hairless = models.IntegerField()
    natural = models.IntegerField()
    rare = models.IntegerField()
    rex = models.IntegerField()
    suppressed_tail = models.IntegerField()
    short_legs = models.IntegerField()
    wikipedia_url = models.URLField(max_length=150)
    hypoallergenic = models.IntegerField()
    reference_image_id = models.CharField(max_length=150)

    def __str__(self):
        return self.external_id | self.name
