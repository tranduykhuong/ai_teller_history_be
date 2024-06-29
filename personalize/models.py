from django.db import models

# Create your models here.
class Personalize(models.Model):
    class Meta:
        db_table = "personalize"
        verbose_name = "Personalize"

    user = models.IntegerField()

    object = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    style = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    purpose = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    meta_data = models.JSONField(
        null=True,
        blank=True,
    )