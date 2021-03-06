# Generated by Django 3.0.6 on 2021-05-06 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_auto_20210505_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_at', models.CharField(default='Team Computers Pvt. Ltd.', max_length=150)),
                ('location', models.CharField(default='India, New Dehli', max_length=50)),
                ('education', models.CharField(default='B.Tech in Computer Science and Engineering', max_length=100)),
                ('descripation', models.CharField(default='Namaste 🙏🏼 I am Software Engineer at Team Computers', max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
