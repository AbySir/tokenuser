# Generated by Django 3.1.1 on 2021-03-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210302_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='creationTime',
            field=models.DateTimeField(default=True),
        ),
    ]
