# Generated by Django 2.2.2 on 2019-10-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_userfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('file_name', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='UserFiles',
        ),
    ]