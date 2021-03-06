# Generated by Django 3.0.2 on 2020-01-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0009_auto_20200118_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='final_summary',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='init_report',
        ),
        migrations.AddField(
            model_name='experiment',
            name='total_infected',
            field=models.IntegerField(default=1, help_text='Amount of people who have contracted the disease at the start.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='total_steps',
            field=models.IntegerField(default=1, help_text='The number of steps for the duration of the whole experiment.'),
            preserve_default=False,
        ),
    ]
