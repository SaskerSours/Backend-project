# Generated by Django 4.2.3 on 2023-07-08 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_report_sent',
            field=models.BooleanField(default=False),
        ),
    ]