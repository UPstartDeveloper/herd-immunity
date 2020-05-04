# Generated by Django 3.0.2 on 2020-05-04 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0016_auto_20200503_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infectednode',
            name='experiment',
            field=models.ForeignKey(help_text='The related Experiment.', on_delete=django.db.models.deletion.CASCADE, to='simulator.Experiment'),
        ),
    ]