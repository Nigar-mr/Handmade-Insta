# Generated by Django 2.2.4 on 2019-08-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm_blog', '0031_auto_20190815_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='addimages',
            name='Images',
            field=models.ImageField(blank=True, null=True, upload_to='shotadd/'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='token',
            field=models.CharField(default='XU6nICQUlz438w8KorHaAFKoASHI6uC2U3vsCW562uMO0SLzfxBCr7N7t3QNpic8sjkJwzyPRD00d2T9m7sor80z1Mmo2QTTiNndc62wjWbZoHziOz4JWB9R', max_length=120),
        ),
    ]
