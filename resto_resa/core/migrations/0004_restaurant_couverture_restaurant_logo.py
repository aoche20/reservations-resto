# Generated by Django 5.2.4 on 2025-07-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_restaurantuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='couverture',
            field=models.ImageField(blank=True, null=True, upload_to='couvertures/'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
