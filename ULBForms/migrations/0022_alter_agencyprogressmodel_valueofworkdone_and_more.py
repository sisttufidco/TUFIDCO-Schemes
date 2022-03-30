# Generated by Django 4.0.3 on 2022-03-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULBForms', '0021_alter_agencyprogressmodel_valueofworkdone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyprogressmodel',
            name='valueofworkdone',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Value of Work done (in lakhs)'),
        ),
        migrations.AlterField(
            model_name='agencysanctionmodel',
            name='work_awarded_amount1',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='With Tax. (Add GST, LWF etc on the above basic cost)', max_digits=8, null=True, verbose_name='Work Order Amount'),
        ),
        migrations.AlterField(
            model_name='agencysanctionmodel',
            name='work_awarded_amount2',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Without Tax (Basic cost/agreed amount, without GST tax etc)', max_digits=8, null=True, verbose_name='Work Order Amount'),
        ),
    ]
