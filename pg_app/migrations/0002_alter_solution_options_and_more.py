# Generated by Django 5.1.4 on 2025-02-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pg_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solution',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='solution',
            name='memory',
            field=models.FloatField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='solution',
            name='runtime',
            field=models.FloatField(blank=True, default=-1),
        ),
        migrations.RemoveField(
            model_name='solution',
            name='attempt_timestamps',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='attempts',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='code',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='date',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='question_slug',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='tags',
        ),
    ]
