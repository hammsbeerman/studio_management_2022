# Generated by Django 3.2.13 on 2022-08-03 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20220624_1142'),
        ('workorders', '0008_alter_workorderinventoryproduct_custom_measurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='workordernoninventoryproduct',
            name='custom_measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='inventory.measurement'),
        ),
        migrations.AddField(
            model_name='workordernoninventoryproduct',
            name='custom_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custom Rate'),
        ),
        migrations.AddField(
            model_name='workordernoninventoryproduct',
            name='measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.measurement'),
        ),
    ]
