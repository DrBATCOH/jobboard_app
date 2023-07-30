from django.db import models


class Expirience(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "expirience"
