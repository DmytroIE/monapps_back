# Generated by Django 5.0.6 on 2024-06-30 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatafeedType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'dftypes',
            },
        ),
        migrations.CreateModel(
            name='DfMeasUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('conv_factor', models.FloatField(default=1.0)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datafeeds.datafeedtype')),
            ],
            options={
                'db_table': 'dfmeasunits',
            },
        ),
        migrations.AddField(
            model_name='datafeedtype',
            name='base_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datafeeds.dfmeasunit'),
        ),
        migrations.CreateModel(
            name='Datafeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('meas_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datafeeds.dfmeasunit')),
            ],
            options={
                'db_table': 'datafeeds',
            },
        ),
    ]
