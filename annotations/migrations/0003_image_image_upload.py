# Generated by Django 3.2.8 on 2021-11-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0002_auto_20211101_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_upload',
            field=models.FileField(default='svss/test.svs', upload_to='svss/'),
            preserve_default=False,
        ),
    ]
