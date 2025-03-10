# Generated by Django 5.1.4 on 2025-03-09 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='questions',
            field=models.ManyToManyField(through='questions.QuestionRelation', to='questions.question'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
