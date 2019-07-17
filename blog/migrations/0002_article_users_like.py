# Generated by Django 2.1 on 2018-12-11 06:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='articles_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]