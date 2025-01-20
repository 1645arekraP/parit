import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pg_site.settings")
django.setup()

from pg_app.utils.LeetcodeWrapper import LeetcodeWrapper
from pg_app.models import Question
import json

x = LeetcodeWrapper()
daily_question = x.get_daily_question().title_slug
question = Question.objects.get(title_slug=daily_question)
question_pools = question.pool_tag
question_pools.remove('LC_DAILY')
question_pools.append('DAILY')
question.save()