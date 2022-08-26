# Generated by Django 3.2.13 on 2022-08-03 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20220624_1142'),
        ('workorders', '0006_auto_20220803_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderinventoryproduct',
            name='measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.measurement'),
        ),
    ]