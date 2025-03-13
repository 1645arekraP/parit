import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=8, max_length=8, prefix='', unique=True)),
                ('group_name', models.CharField(default='Unnamed Group', max_length=254)),
                ('question_pool_type', models.CharField(choices=[('DAILY', 'Daily Question'), ('BLIND_75', 'Blind 75'), ('NEETCODE_150', 'Neetcode 150'), ('NEETCODE_250', 'Neetcode 250'), ('LC_ALL', 'Leetcode All')], default='DAILY', max_length=36)),
                ('question_pool_type', models.CharField(choices=[('DAILY', 'Daily Question'), ('BLIND_75', 'Blind 75'), ('NEETCODE_150', 'Neetcode 150'), ('NEETCODE_250', 'Neetcode 250'), ('LC_ALL', 'Leetcode All'), ('CUSTOM', 'Custom Pool')], default='DAILY', max_length=36)),
                ('members', models.ManyToManyField(related_name='study_groups', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_groups', to='questions.question')),
            ],
        ),
        migrations.CreateModel(
            name='StudyGroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('OWNER', 'Owner'), ('ADMIN', 'Admin'), ('MEMBER', 'Member')], default='MEMBER', max_length=10)),
                ('study_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.studygroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('study_group', 'user')},
            },
        ),
        migrations.AddField(
            model_name='studygroup',
            name='members',
            field=models.ManyToManyField(related_name='study_groups', through='groups.StudyGroupMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]
