# Generated by Django 4.1.4 on 2023-01-25 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_goalsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalsmodel',
            name='Timeline_objective',
            field=models.CharField(choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031')], default='2023', max_length=20),
        ),
    ]