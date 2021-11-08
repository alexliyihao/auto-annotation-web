# Generated by Django 3.2.8 on 2021-11-08 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0006_alter_image_image_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='annotator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='annotations.user'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='image',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='annotations.image'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='update_date',
            field=models.DateTimeField(blank=True, verbose_name='date submit this annotation'),
        ),
    ]