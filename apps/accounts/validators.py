from django.core.exceptions import ValidationError

def validate_leetcode_username(value):
    if not value.isalnum():
        raise ValidationError('LeetCode username must be alphanumeric.')
