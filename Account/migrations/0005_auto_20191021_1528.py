# Generated by Django 2.2.2 on 2019-10-21 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_auto_20191020_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='file',
            field=models.FilePathField(max_length=200),
        ),
    ]
