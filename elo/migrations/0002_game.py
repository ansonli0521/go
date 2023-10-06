# Generated by Django 2.0.1 on 2023-10-06 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=1)),
                ('game_date', models.DateField()),
                ('black', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='black', to='elo.Player')),
                ('white', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='white', to='elo.Player')),
            ],
        ),
    ]
