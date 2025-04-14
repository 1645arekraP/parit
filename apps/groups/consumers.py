from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.template.loader import get_template
import json
import asyncio
from django_redis import get_redis_connection

class GroupConsumer(AsyncWebsocketConsumer):
    #TODO: Modal isnt updated when refreshing group solutions
    async def connect(self):
        from apps.groups.models import StudyGroup

        # Check if user is authenticated
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        # Redis connection used for caching
        self.redis = get_redis_connection()

        # User and group setup
        invite_code = self.scope['url_route']['kwargs']['invite_code']
        self.group = await sync_to_async(StudyGroup.objects.get)(invite_code=invite_code)
        self.group_name = invite_code

        # Add user to websocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Store active group along with user count in redis cache
        print(f"Redis: {self.redis.hgetall('active_groups')}")
        self.redis.hincrby("active_groups", invite_code, 1)
        print(f"Redis: {self.redis.hgetall('active_groups')}")
        # Accept connection
        await self.accept()

        # Debug stuff
        print(f"{self.user.username} is now connected to group: {self.group.invite_code} ({self.group.group_name})")
        #print(f"Redis: {self.redis.smembers(f'active_group:{invite_code}')}")

    async def receive(self, text_data):
        # This will contain chat logic
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        # Update redis cache
        self.redis.hincrby("active_groups", self.group.invite_code, -1)
        active_group_count = self.redis.hget("active_groups", self.group.invite_code)
        active_group_count = int(active_group_count) if active_group_count else 0
        if active_group_count <= 0:
            # Delete group from redis cache if no users are connected
            self.redis.hdel("active_groups", self.group.invite_code)

        # Debug stuff
        print(f"{self.user.username} is now disconnected from group: {self.group.invite_code} ({self.group.group_name})")
        print(f"Redis: {self.redis.hgetall('active_groups')}")


    async def updated_solutions(self, event):
        #print(f"Group data: {event['html']}")
        await self.send(text_data=event['html'])

        print("Updated solutions sent")

    async def updated_question(self, event):
        # TODO: add send status
        await self.send(text_data=event['status'])