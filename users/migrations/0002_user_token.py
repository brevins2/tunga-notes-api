# Generated by Django 4.2.6 on 2023-10-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
