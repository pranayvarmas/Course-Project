# Generated by Django 3.1.3 on 2020-12-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0003_auto_20201207_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
