# Generated by Django 4.0.3 on 2022-03-23 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ULBForms', '0016_ulbsanctionreporterror_agencysanctionmodel_district_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ULBProgressIncompleted',
        ),
        migrations.DeleteModel(
            name='ULBSanctionReportError',
        ),
    ]
