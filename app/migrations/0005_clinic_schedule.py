# Generated by Django 4.2.7 on 2023-11-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_chat_created_at_alter_chat_message_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic_Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
