# Generated by Django 5.1.4 on 2025-01-20 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, to='labels.label'),
        ),
    ]
