# Generated by Django 4.2.7 on 2023-11-18 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0006_estimates_estimateitems_estimate_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurring_invoice',
            name='cust_name',
        ),
        migrations.RemoveField(
            model_name='recurring_invoice',
            name='items',
        ),
        migrations.RemoveField(
            model_name='recurring_invoice',
            name='user',
        ),
        migrations.DeleteModel(
            name='recur_itemtable',
        ),
        migrations.DeleteModel(
            name='Recurring_invoice',
        ),
    ]
