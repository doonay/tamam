# Generated by Django 4.2.2 on 2023-06-11 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tamam_app', '0002_delete_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='XboxGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tamam_app.game')),
            ],
            bases=('tamam_app.game',),
        ),
    ]
