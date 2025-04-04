from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
            'class': 'input validator',
            'type': 'password',
            'required placeholder': 'Enter your password',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
            'minlength': 8,
            'maxlength': 128,
        }))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={
            'class': 'input validator',
            'type': 'password',
            'required placeholder': 'Enter your password',
            'minlength': 8,
            'maxlength': 128,
            'title': 'Passwords must match.',
        }))
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'input validator',
            'type': 'input',
            'required placeholder': 'Username',
            'pattern': '[A-Za-z][A-Za-z0-9\-]*',
            'minlength': 3,
            'maxlength': 30,
            'title': 'Only letters, numbers or dash',
            })
    )


    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        widgets = {
            "email": forms.EmailInput(attrs={
                'class': 'input validator',
                'required placeholder': 'Enter your email',
                'type': 'email',
            }),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.leetcode_username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your username',
        }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data
    
class AddFriendForm(forms.Form):
    form_id = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'input',
            'value': 'add_friend'
        })
    )
    friend_email = forms.EmailField(
        label="Friend's Email",
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Enter friend\'s email'
        })
    )

class SettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture', 'email', 'leetcode_username', 'newsletter']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered',
                'placeholder': 'Enter your email'
            }),
            'newsletter': forms.CheckboxInput(attrs={
                'class': 'checkbox'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered',
                'placeholder': 'Last Name'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'file-input',
                'type': 'file',
                'placeholder': 'Profile Picture'
            }),
            'leetcode_username': forms.TextInput(attrs={
                'class': 'input input-bordered',
                'placeholder': 'LeetCode Username'
            }),
        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Current Password", widget=forms.PasswordInput(attrs={
            'class': 'input validator',
            'type': 'password',
            'required placeholder': 'Enter your password',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
            'minlength': 8,
            'maxlength': 128,
        }))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={
            'class': 'input validator',
            'type': 'password',
            'required placeholder': 'Enter your new password',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
            'minlength': 8,
            'maxlength': 128,
        }))
    new_password2 = forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput(attrs={
            'class': 'input validator',
            'type': 'password',
            'required placeholder': 'Confirm your new password',
            'minlength': 8,
            'maxlength': 128,
            'title': 'Passwords must match.',
        }))

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords don't match")
        if len(new_password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if len(new_password1) > 128:
            raise forms.ValidationError("Password must be at most 128 characters long.")
        if not any(char.isdigit() for char in new_password1):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.isupper() for char in new_password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in new_password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        return cleaned_data