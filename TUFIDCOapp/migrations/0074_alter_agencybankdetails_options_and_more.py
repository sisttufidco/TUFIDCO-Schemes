# Generated by Django 4.0 on 2022-01-15 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0073_agencysanctionmodel_fundrelease'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencybankdetails',
            options={'verbose_name': 'Agency Bank Detail', 'verbose_name_plural': 'Agency Bank Details'},
        ),
        migrations.AddField(
            model_name='agencybankdetails',
            name='passbookupload',
            field=models.FileField(help_text='Please upload a scanned copy of front page of passbook', null=True, upload_to='passbook/', verbose_name='Passbook Front Page Photo'),
        ),
    ]
