# Generated by Django 4.2.7 on 2024-06-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_buyer_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
