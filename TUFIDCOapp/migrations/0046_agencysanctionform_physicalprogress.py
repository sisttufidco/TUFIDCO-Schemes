# Generated by Django 4.0 on 2022-01-05 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0045_remove_physicalprogress_agencysanctionform_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencySanctionForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Latitude', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Latitude')),
                ('Longitude', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Longitude')),
                ('physicalProgress', models.TextField(null=True, verbose_name='Physical Progress')),
                ('value', models.CharField(max_length=100, null=True, verbose_name='Value of Work Done')),
                ('expenditure', models.CharField(max_length=100, null=True, verbose_name='Expenditure')),
                ('physicalProgressPhoto', models.FileField(blank=True, help_text='Upload site photos indicating the Latitude and Longitude of the site, as generated by Google Maps', null=True, upload_to='', verbose_name='Upload Photo')),
                ('ProjectName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Project_Name', to='TUFIDCOapp.mastersanctionform')),
                ('Project_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProjectID', to='TUFIDCOapp.mastersanctionform')),
                ('scheme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TUFIDCOapp.scheme')),
            ],
        ),
        migrations.CreateModel(
            name='physicalProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physicalProgressPhoto', models.FileField(null=True, upload_to='physicalProgress/', verbose_name='Physical Process Photo')),
                ('AgencySanctionForm', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='TUFIDCOapp.agencysanctionform')),
            ],
        ),
    ]
