# Generated by Django 5.0.3 on 2024-04-09 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
