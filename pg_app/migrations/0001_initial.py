# Generated by Django 5.1.4 on 2025-02-13 18:31

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=36, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_tags', models.JSONField(blank=True, null=True)),
                ('ac_rate', models.FloatField()),
                ('content', models.CharField(blank=True, max_length=5012, null=True)),
                ('difficulty', models.CharField(max_length=1024)),
                ('is_paid', models.BooleanField(default=False)),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=1024)),
                ('title_slug', models.SlugField(max_length=255, unique=True)),
                ('pool_tag', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_is_active', models.BooleanField(default=True)),
                ('acceptance_rate', models.FloatField(default=0.0)),
                ('streak', models.IntegerField(default=0)),
                ('friends', models.ManyToManyField(blank=True, to='pg_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=8, max_length=8, prefix='', unique=True)),
                ('group_name', models.CharField(default='Unnamed Group', max_length=254)),
                ('question_pool_type', models.CharField(choices=[('DAILY', 'Daily Question'), ('BLIND_75', 'Blind 75'), ('NEETCODE_150', 'Neetcode 150'), ('NEETCODE_250', 'Neetcode 250'), ('LC_ALL', 'Leetcode All'), ('CUSTOM', 'Custom Pool')], default='DAILY', max_length=36)),
                ('members', models.ManyToManyField(related_name='user_groups', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='pg_app.question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('solved', 'Solved'), ('excelled', 'Excelled'), ('struggled', 'Struggled'), ('unsolved', 'Unsolved'), ('strugglingToSolve', 'StrugglingToSolve')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pg_app.question')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pg_app.profile')),
            ],
            options={
                'unique_together': {('profile', 'question', 'relation_type')},
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='questions',
            field=models.ManyToManyField(through='pg_app.QuestionRelation', to='pg_app.question'),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_slug', models.IntegerField(default=1)),
                ('memory', models.FloatField()),
                ('runtime', models.FloatField()),
                ('tags', models.JSONField()),
                ('accepted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('attempts', models.IntegerField(default=0)),
                ('attempt_timestamps', models.JSONField(default=list)),
                ('code', models.TextField(blank=True)),
                ('question', models.ForeignKey(default='two-sum', on_delete=django.db.models.deletion.CASCADE, to='pg_app.question')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='pg_app.profile')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('profile', 'question')},
            },
        ),
    ]
