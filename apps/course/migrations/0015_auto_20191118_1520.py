# Generated by Django 2.2.7 on 2019-11-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_auto_20191118_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='course/%Y/%m', verbose_name='封面图'),
        ),
    ]
