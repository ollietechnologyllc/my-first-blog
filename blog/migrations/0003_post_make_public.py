# Generated by Django 2.2.20 on 2021-05-25 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210524_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='make_public',
            field=models.BooleanField(null=True),
        ),
    ]