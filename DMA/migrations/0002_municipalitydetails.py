# Generated by Django 4.0.3 on 2022-03-19 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DMA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MunicipalityDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sno', models.IntegerField(null=True, verbose_name='S.No')),
                ('municipality_name', models.CharField(max_length=40, null=True, verbose_name='Name of Municipality')),
                ('district', models.CharField(max_length=40, null=True, verbose_name='District')),
                ('region', models.CharField(max_length=40, null=True, verbose_name='Region')),
                ('email_id1', models.EmailField(max_length=40, null=True, verbose_name='Email ID')),
                ('email_id2', models.EmailField(blank=True, max_length=40, null=True, verbose_name='Alternative Email ID')),
                ('mc', models.IntegerField(null=True, verbose_name='Municipal Commissioner Phone Number')),
                ('me', models.IntegerField(null=True, verbose_name='Municipal Engineer Phone Number')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
