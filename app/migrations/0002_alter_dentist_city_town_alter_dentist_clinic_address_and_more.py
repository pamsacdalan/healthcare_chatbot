# Generated by Django 4.2.7 on 2023-11-22 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dentist',
            name='city_town',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='clinic_address',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='clinic_name',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='clinic_schedule',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='contact_number',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='dentist_name',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='province',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='region',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='zipcode',
            field=models.IntegerField(null=True),
        ),
    ]