# Generated by Django 3.0.6 on 2021-05-15 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_userdetails_github_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedblogs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_blog', to=settings.AUTH_USER_MODEL),
        ),
    ]
