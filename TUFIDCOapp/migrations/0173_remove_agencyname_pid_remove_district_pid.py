# Generated by Django 4.0.4 on 2022-05-20 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0172_delete_receiptform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencyname',
            name='Pid',
        ),
        migrations.RemoveField(
            model_name='district',
            name='Pid',
        ),
    ]
