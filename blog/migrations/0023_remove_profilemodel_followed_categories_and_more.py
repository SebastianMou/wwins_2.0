# Generated by Django 4.1.4 on 2023-02-08 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_profilemodel_followed_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilemodel',
            name='followed_categories',
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='followed_categories',
            field=models.ManyToManyField(null=True, related_name='followed_by', to='blog.category'),
        ),
    ]
