# Generated by Django 3.2.8 on 2021-11-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0009_annotation_w3c_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
