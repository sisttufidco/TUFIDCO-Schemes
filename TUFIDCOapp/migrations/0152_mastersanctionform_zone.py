# Generated by Django 4.0.3 on 2022-03-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0151_delete_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersanctionform',
            name='zone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Zone'),
        ),
    ]
