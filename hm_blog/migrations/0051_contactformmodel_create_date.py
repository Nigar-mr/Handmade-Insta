# Generated by Django 2.2.4 on 2019-08-21 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm_blog', '0050_auto_20190820_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformmodel',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
