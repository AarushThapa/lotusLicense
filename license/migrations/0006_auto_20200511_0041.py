# Generated by Django 3.0.5 on 2020-05-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0005_auto_20200511_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='timeout',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]