# Generated by Django 4.0.4 on 2022-05-20 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_receiptform'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthWiseReport',
            fields=[
            ],
            options={
                'verbose_name': 'Month Wise Report',
                'verbose_name_plural': 'Month Wise Report',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Accounts.releaserequestmodel',),
        ),
    ]
