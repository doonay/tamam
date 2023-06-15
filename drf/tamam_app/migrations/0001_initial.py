# Generated by Django 4.2.2 on 2023-06-14 10:05

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('platforms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('base_price', models.IntegerField()),
                ('discounted_price', models.IntegerField()),
                ('discount', models.SmallIntegerField()),
                ('img', models.CharField(max_length=255)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='tamam_app.platform')),
            ],
        ),
    ]
