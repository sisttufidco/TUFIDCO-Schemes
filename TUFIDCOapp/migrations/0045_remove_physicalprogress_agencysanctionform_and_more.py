# Generated by Django 4.0 on 2022-01-05 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0044_agencysanctionform_expenditure_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalprogress',
            name='AgencySanctionForm',
        ),
        migrations.DeleteModel(
            name='AgencySanctionForm',
        ),
        migrations.DeleteModel(
            name='physicalProgress',
        ),
    ]
