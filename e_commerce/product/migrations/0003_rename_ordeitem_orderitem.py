# Generated by Django 5.0 on 2024-01-02 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_order_ordeitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdeItem',
            new_name='OrderItem',
        ),
    ]
