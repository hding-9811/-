from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser





class Computer(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=256, verbose_name="品牌")

    class Meta:
        db_table = "bz_computer"
        verbose_name = "电脑"
        verbose_name_plural = "电脑"

    def __str__(self):
        return self.name
