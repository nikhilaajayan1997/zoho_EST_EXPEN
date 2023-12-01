# Generated by Django 4.2.7 on 2023-11-30 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0017_expensee_expense_comments_attache'),
    ]

    operations = [
        migrations.CreateModel(
            name='deletedexpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(max_length=50)),
                ('cid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.company_details')),
            ],
        ),
    ]
