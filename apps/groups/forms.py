from django import forms
from ..accounts.models import CustomUser
from .models import StudyGroup

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
        model = StudyGroup
        exclude = ["invite_code"]
        fields = ["group_name", "question_pool_type"]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = self.instance.members.all()  # Filter by group
        self.fields['invite_code'].initial = self.instance.invite_code