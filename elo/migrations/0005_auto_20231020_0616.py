# Generated by Django 2.0.1 on 2023-10-20 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elo', '0004_player_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='lost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='win',
            field=models.IntegerField(default=0),
        ),
    ]
