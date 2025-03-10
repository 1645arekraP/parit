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
    
