from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'grow', 'placeholder': 'Enter your username'})
    )


    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        widgets = {
            "email": forms.EmailInput(attrs={
                'class': 'grow',
                'placeholder': 'Enter your email',
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
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your email',
        }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))