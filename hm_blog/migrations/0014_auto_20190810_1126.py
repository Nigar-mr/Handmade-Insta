# Generated by Django 2.2.4 on 2019-08-10 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm_blog', '0013_auto_20190810_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialsettings',
            name='value',
        ),
        migrations.AlterField(
            model_name='verification',
            name='token',
            field=models.CharField(default='XdZF4BlfwXz3qAVTTBAWqxhHNAwakKbvuehRZk7Mk6t2EaHb8CtHuWapWE0N21UAkqmxgRv7bKZeISA1byuUVg8SNPgiNZwwASNyz0pd7q3jr3aANNTs8bD4', max_length=120),
        ),
    ]
