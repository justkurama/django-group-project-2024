# Generated by Django 4.2.16 on 2024-10-17 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paypal_transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
