# Generated by Django 4.2.7 on 2024-07-09 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_contact_newslatter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='massage',
            new_name='message',
        ),
    ]
