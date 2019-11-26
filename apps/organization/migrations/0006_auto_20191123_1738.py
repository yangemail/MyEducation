# Generated by Django 2.2.7 on 2019-11-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20191118_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorganization',
            name='tutorial_nums',
            field=models.PositiveIntegerField(default=0, verbose_name='教程数量'),
        ),
        migrations.AlterField(
            model_name='courseorganization',
            name='course_nums',
            field=models.PositiveIntegerField(default=0, verbose_name='课程数量'),
        ),
    ]