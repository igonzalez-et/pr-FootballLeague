# Generated by Django 4.1.7 on 2023-04-14 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagueApp', '0006_league'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league', to='leagueApp.league'),
        ),
    ]
