# Generated by Django 3.0.2 on 2020-05-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='desc',
            field=models.TextField(default='', max_length=500),
        ),
    ]
