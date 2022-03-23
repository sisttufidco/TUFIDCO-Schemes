# Generated by Django 4.0.3 on 2022-03-23 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0151_delete_location'),
        ('reports', '0004_progressnotentered'),
    ]

    operations = [
        migrations.CreateModel(
            name='SanctionNotEntered',
            fields=[
            ],
            options={
                'verbose_name': 'Sanction Detail Not Entered',
                'verbose_name_plural': 'Sanction Details Not Entered',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('TUFIDCOapp.mastersanctionform',),
        ),
        migrations.AlterModelOptions(
            name='progressnotentered',
            options={'verbose_name': 'Progress Detail Not Entered', 'verbose_name_plural': 'Progress Details Not Entered'},
        ),
    ]
