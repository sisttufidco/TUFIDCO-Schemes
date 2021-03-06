# Generated by Django 4.0 on 2022-01-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0041_rename_physicalprogress_agencysanctionform_physicalprogressphoto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalprogress',
            name='physicalProgress',
        ),
        migrations.AddField(
            model_name='agencysanctionform',
            name='physicalProgress',
            field=models.TextField(null=True, verbose_name='Physical Progress'),
        ),
        migrations.AddField(
            model_name='physicalprogress',
            name='physicalProgressPhoto',
            field=models.FileField(null=True, upload_to='physicalProgress/', verbose_name='Physical Process Photo'),
        ),
        migrations.AlterField(
            model_name='agencysanctionform',
            name='physicalProgressPhoto',
            field=models.FileField(blank=True, help_text='Upload site photos indicating the Latitude and Longitude of the site, as generated by Google Maps', null=True, upload_to='', verbose_name='Upload Photo'),
        ),
    ]
