# Generated by Django 4.0.3 on 2022-03-20 10:32

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ULBForms', '0009_alter_agencyprogressmodel_nc_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ULBProgressReport',
            fields=[
            ],
            options={
                'verbose_name': 'ULB Progress Report',
                'verbose_name_plural': 'ULB Progress Report',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ULBForms.agencyprogressmodel',),
        ),
    ]
