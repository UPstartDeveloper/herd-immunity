# Generated by Django 3.0.2 on 2020-05-03 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0014_remove_timestep_vaccinated_population'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfectedNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifer', models.CharField(help_text='Identifier of the person/virus in experiment.', max_length=10000)),
                ('children', models.ForeignKey(help_text='People infected by this node.', on_delete=django.db.models.deletion.CASCADE, to='simulator.InfectedNode')),
                ('experiment', models.OneToOneField(help_text='The related Experiment.', on_delete=django.db.models.deletion.CASCADE, to='simulator.Experiment')),
            ],
        ),
    ]
