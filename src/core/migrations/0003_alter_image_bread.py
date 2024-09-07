# Generated by Django 5.1.1 on 2024-09-07 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='bread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.bread'),
        ),
    ]
