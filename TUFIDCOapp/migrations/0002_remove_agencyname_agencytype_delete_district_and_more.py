# Generated by Django 4.0 on 2021-12-31 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencyname',
            name='AgencyType',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='AgencyName',
        ),
        migrations.DeleteModel(
            name='AgencyType',
        ),
    ]
