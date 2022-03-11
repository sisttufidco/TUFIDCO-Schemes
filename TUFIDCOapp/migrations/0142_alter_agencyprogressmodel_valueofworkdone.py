# Generated by Django 4.0.3 on 2022-03-11 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0141_alter_agencyprogressmodel_valueofworkdone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyprogressmodel',
            name='valueofworkdone',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Value of Work done (in lakhs)'),
        ),
    ]
