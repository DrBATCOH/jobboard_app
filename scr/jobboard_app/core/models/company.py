from django.db import models


class Company(models.Model):
    name = models.CharField(unique=True, max_length=30)
    employees_number = models.PositiveIntegerField()
    logo = models.ImageField(upload_to="companies/logo", null=True)

    class Meta:
        db_table = "companies"
