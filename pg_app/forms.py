from django import forms
from .models import CustomUser, UserGroup
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={
            'class': 'grow',
            'placeholder': 'Enter your password',
        }))

    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        widgets = {
            "email": forms.EmailInput(attrs={
                'class': 'grow',
                'placeholder': 'Enter your email',
            }),
            "username": forms.TextInput(attrs={
                'class': 'grow',
                'placeholder': 'Enter your username',
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

class GroupSettingsForm(forms.ModelForm):
    invite_code = forms.CharField(
        required=False,  # Don't require this field to be filled out by the user
        disabled=True,   # Disable editing, so it appears read-only
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make the field readonly in the HTML
    )
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  # Default to none, update dynamically
    )
    
    class Meta:
        model = UserGroup
        exclude = ["invite_code"]
        fields = ["group_name", "question_pool_type"]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = self.instance.members.all()  # Filter by group
        self.fields['invite_code'].initial = self.instance.invite_code