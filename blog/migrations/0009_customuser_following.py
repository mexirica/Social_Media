# Generated by Django 4.2.1 on 2023-05-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_customuser_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]
