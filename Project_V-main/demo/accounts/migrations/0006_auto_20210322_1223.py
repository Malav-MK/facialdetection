# Generated by Django 3.1.6 on 2021-03-22 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210319_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='password1',
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.IntegerField(),
        ),
    ]
