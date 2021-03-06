# Generated by Django 3.2.8 on 2021-11-10 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0012_auto_20211109_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='annotation_class',
            field=models.CharField(blank=True, choices=[('Glomerulus', 'Glomerulus'), ('Arteries', 'Arteries'), ('Tubules', 'Tubules'), ('Interstitium', 'Interstitium')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='annotation',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
