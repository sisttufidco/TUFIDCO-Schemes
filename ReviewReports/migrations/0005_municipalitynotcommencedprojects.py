# Generated by Django 4.0.4 on 2022-05-26 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ULBForms', '0046_alter_agencyprogressmodel_nc_choices'),
        ('ReviewReports', '0004_townpanchayatinprogressprojects'),
    ]

    operations = [
        migrations.CreateModel(
            name='MunicipalityNotCommencedProjects',
            fields=[
            ],
            options={
                'verbose_name': 'DMA Not Commenced Projects',
                'verbose_name_plural': 'DMA Not Commenced Projects',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ULBForms.agencyprogressmodel',),
        ),
    ]
