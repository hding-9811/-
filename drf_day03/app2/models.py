from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256)

    class Meta:
        db_table = "bz_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
