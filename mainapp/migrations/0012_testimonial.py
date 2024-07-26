# Generated by Django 4.2.7 on 2024-07-19 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_rename_massage_contact_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('pic', models.ImageField(upload_to='uploads/testimonials')),
            ],
        ),
    ]
