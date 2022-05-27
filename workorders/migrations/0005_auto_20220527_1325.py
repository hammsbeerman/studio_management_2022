# Generated by Django 3.2.13 on 2022-05-27 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0004_alter_workorderservice_custom_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderservice',
            name='billable_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Billable Time'),
        ),
        migrations.AlterField(
            model_name='workorderservice',
            name='default_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Default Rate'),
        ),
        migrations.AlterField(
            model_name='workorderservice',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Description'),
        ),
    ]
