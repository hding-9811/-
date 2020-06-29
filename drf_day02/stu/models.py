from django.db import models

# Create your models here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class Student(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other"),
    )

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    num = models.IntegerField()

    class Meta:
        db_table = "bz_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
