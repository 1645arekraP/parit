from django.test import TestCase
from django.contrib.auth import authenticate
from .models import CustomUser, UserGroup, Solution, Profile
from django.db.utils import IntegrityError

class UserTests(TestCase):
    # Things to be teseted
    # All attributes: Username, Email, and password are all required

    def test_create_valid_user(self):
        created_user = CustomUser.objects.create_user("test@gmail.com", "username_test", "password_test")
        self.assertEqual(created_user.email, "test@gmail.com")
        self.assertEqual(created_user.username, "username_test")
        # User authenticate to test that both this works and that the password field works
        authenticated_user = authenticate(email="test@gmail.com", password="password_test")
        self.assertEqual(created_user, authenticated_user)
        self.assertTrue(created_user.is_authenticated)
        self.assertTrue(created_user.is_active)
        self.assertFalse(created_user.is_staff)
        self.assertFalse(created_user.is_superuser)
    
    def test_create_valid_superuser(self):
        created_user = CustomUser.objects.create_superuser(
            "test@gmail.com", "username_test", "password_test", 
            is_superuser=True, 
            is_staff=True)
        self.assertEqual(created_user.email, "test@gmail.com")
        self.assertEqual(created_user.username, "username_test")
        # User authenticate to test that both this works and that the password field works
        authenticated_user = authenticate(email="test@gmail.com", password="password_test")
        self.assertEqual(created_user, authenticated_user)
        self.assertTrue(created_user.is_authenticated)
        self.assertTrue(created_user.is_active)
        self.assertTrue(created_user.is_staff)
        self.assertTrue(created_user.is_superuser)

    def test_create_invalid_superuser(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                "test@gmail.com", "username_test", "password_test", 
                is_superuser=True, 
                is_staff=False)
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                "test@gmail.com", "username_test", "password_test", 
                is_superuser=False, 
                is_staff=True)

    def test_create_invalid_user(self):
        # Note: Password validators are not applied at the model level
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user("", "username_test", "password_test")
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user("test@gmail.com", "", "password_test")
        
    def test_create_existing_user(self):
        CustomUser.objects.create_user("test@gmail.com", "username1_test", "password_test")
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user("test@gmail.com", "username2_test", "password_test")

    def test_create_username_not_unique(self):
        user1 = CustomUser.objects.create_user("test1@gmail.com", "username_test", "password_test")
        user2 = CustomUser.objects.create_user("test2@gmail.com", "username_test", "password_test")
        self.assertEqual(user1.username, user2.username)
    
class GroupTests(TestCase):
    def setUp(self):
        CustomUser.objects.create_user("test1@gmail.com", "username1_test", "password_test")
        CustomUser.objects.create_user("test2@gmail.com", "username2_test", "password_test")
        CustomUser.objects.create_user("test3@gmail.com", "username3_test", "password_test")
        
    
    def test_create_valid_group(self):
        group_1 = UserGroup.objects.create()
        self.assertEqual(group_1.group_name, "Unnamed Group")
        self.assertEqual(group_1.question_pool_type, "DAILY")
        self.assertIsNotNone(group_1.invite_code)
    
    def test_create_invite_code_collision(self):
        group_1 = UserGroup.objects.create()
        group_2 = UserGroup.objects.create()
        group_1.invite_code = 12345678
        group_2.invite_code = 12345678
        group_1.save()
        group_2.save()
        self.assertNotEqual(group_1.invite_code, group_2.invite_code)
    
    def test_users_in_groups(self):
        pass

# TODO: Need more test cases