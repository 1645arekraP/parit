import os
import sys
import django
import json
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pg_site.settings")
django.setup()

from pg_app.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from pg_app.models import Question
from pg_app.utils.scripts.question_pools import blind_75, neetcode_150, neetcode_250

Question.objects.all().delete() 
lcw = LeetcodeWrapper()
data = asyncio.run(lcw.get_questions(limit=30))
questions = data.questions

for q in questions:
    question_pools = ['LC_ALL']
    if q.title_slug in blind_75:
        question_pools.append("BLIND_75")
    if q.title_slug in neetcode_150:
        question_pools.append("NEETCODE_150")
    if q.title_slug in neetcode_250:
        question_pools.append("NEETCODE_250")
    try:
        Question.objects.create(
            ac_rate = q.ac_rate,
            content = q.content,
            difficulty = q.difficulty,
            is_paid = q.is_paid,
            link = q.link,
            title = q.title,
            title_slug = q.title_slug,
            topic_tags = q.topic_tags,
            pool_tag=question_pools
        )
    except Exception as e:
        print(e)