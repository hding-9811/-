# Generated by Django 2.0.6 on 2020-07-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='banner', verbose_name='轮播图图片'),
        ),
    ]