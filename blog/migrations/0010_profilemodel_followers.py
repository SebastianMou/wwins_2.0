# Generated by Django 4.1.4 on 2023-01-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='followers',
            field=models.ManyToManyField(related_name='following', through='blog.Follower', to='blog.profilemodel'),
        ),
    ]
