# Generated by Django 3.0.5 on 2020-05-10 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0003_auto_20200510_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='owner',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='timeout',
            field=models.DateTimeField(null=True),
        ),
    ]