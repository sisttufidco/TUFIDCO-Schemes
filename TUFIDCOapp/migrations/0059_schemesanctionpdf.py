# Generated by Django 4.0 on 2022-01-07 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0058_rename_pdf1_scheme_page_pdf_guidelines_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemeSanctionPdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdf/')),
                ('Pdf_name', models.CharField(max_length=200, null=True, verbose_name='PDF Name')),
                ('scheme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TUFIDCOapp.scheme')),
            ],
        ),
    ]
