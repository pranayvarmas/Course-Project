# Generated by Django 3.1.3 on 2020-12-07 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0002_profile_picture2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(upload_to='uploads_cdn/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture2',
            field=models.FileField(default='', upload_to='input/'),
        ),
    ]