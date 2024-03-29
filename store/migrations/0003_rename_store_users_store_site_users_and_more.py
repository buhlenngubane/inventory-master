# Generated by Django 4.2.11 on 2024-03-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20190617_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='store_users',
            new_name='site_users',
        ),
        migrations.RemoveField(
            model_name='store',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='store',
            name='number_of_items',
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Site name'),
        ),
    ]
