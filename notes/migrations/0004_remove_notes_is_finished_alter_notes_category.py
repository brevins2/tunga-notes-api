# Generated by Django 4.2.6 on 2023-10-26 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_notes_created_time_alter_notes_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='is_finished',
        ),
        migrations.AlterField(
            model_name='notes',
            name='category',
            field=models.CharField(max_length=200),
        ),
    ]
