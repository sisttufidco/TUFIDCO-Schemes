# Generated by Django 4.0 on 2022-01-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0090_alter_agencysanctionmodel_wd_awarded'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencysanctionmodel',
            options={'verbose_name': 'Agency Sanction Detail', 'verbose_name_plural': 'Agency Sanction Details'},
        ),
        migrations.AlterField(
            model_name='mastersanctionform',
            name='ProjectName',
            field=models.TextField(blank=True, null=True, verbose_name='Name of the Work'),
        ),
    ]
