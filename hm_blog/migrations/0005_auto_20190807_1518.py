# Generated by Django 2.2.4 on 2019-08-07 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm_blog', '0004_auto_20190807_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='shotdetails',
            name='Title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='verification',
            name='token',
            field=models.CharField(default='24yigU5iPOKWZtDPoH2SU2gUWn2HcC5r4oyMNgOtdMPEwQ7Zkmayp4XZUTZIjfua43Mkb7rU9lrxwOxU3czSoM13YUIkn79c5W71q0uW5rrJncqYJtd6CgRX', max_length=120),
        ),
    ]
