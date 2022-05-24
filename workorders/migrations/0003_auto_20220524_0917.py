# Generated by Django 3.2.13 on 2022-05-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0002_alter_workorder_workorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Description'),
        ),
    ]
