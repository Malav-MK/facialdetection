# Generated by Django 2.2.15 on 2021-03-19 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='confirm_date',
        ),
    ]