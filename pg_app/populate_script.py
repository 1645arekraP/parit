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

lcw = LeetcodeWrapper()
data = asyncio.run(lcw.get_accepted_solutions(username="parkera", limit=5))
for s in data.solutions:
    print(f"{s.title}: {s.status}")



"""for q in questions['questions']:
    question_pools = ['LC_ALL']
    if q['titleSlug'] in blind_75:
        question_pools.append("BLIND_75")
    if q['titleSlug'] in neetcode_150:
        question_pools.append("NEETCODE_150")
    if q['titleSlug'] in neetcode_250:
        question_pools.append("NEETCODE_250")
    topic_tags = []
    for tag in q['topicTags']:
        topic_tags.append(tag['name'])
    try:
        Question.objects.create(
            ac_rate = q['acRate'],
            content = q['content'],
            difficulty = q['difficulty'],
            is_paid = q['paidOnly'],
            link = "",
            title = q['title'],
            title_slug = q['titleSlug'],
            topic_tags = topic_tags,
            pool_tag=question_pools
        )
    except Exception as e:
        print(e)"""