# Generated by Django 4.0.5 on 2022-06-11 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ULBForms', '0058_alter_agencyprogressmodel_fundrelease_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencybankdetails',
            name='IFSC_code',
        ),
        migrations.RemoveField(
            model_name='agencybankdetails',
            name='account_number',
        ),
        migrations.RemoveField(
            model_name='agencybankdetails',
            name='passbookupload',
        ),
    ]
