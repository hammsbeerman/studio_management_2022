# Generated by Django 3.2.13 on 2022-08-03 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20220624_1142'),
        ('workorders', '0007_alter_workorderinventoryproduct_measurement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderinventoryproduct',
            name='custom_measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='inventory.measurement'),
        ),
    ]