# Generated by Django 4.1.4 on 2023-02-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_remove_profilemodel_followed_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='followed_categories',
            field=models.ManyToManyField(related_name='followed_by', to='blog.category'),
        ),
    ]
