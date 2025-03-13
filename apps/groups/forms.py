from django import forms
from apps.accounts.models import CustomUser
from .models import StudyGroup
from apps.questions.models import Question
from apps.groups.services.group_service import create_group

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

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(
        help_text='Give your study group a name'
    )
    question_pool_type = forms.ChoiceField(
        choices=StudyGroup.QUESTION_POOL_TYPE_CHOICES,
        help_text='Choose the type of questions for your group'
    )
    initial_members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        required=False,
        label="Add Friends",
        help_text="Select friends to add to your group"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['initial_members'].queryset = self.user.friends.all()

    def save(self):
        group = create_group(
            user=self.user,
            group_name=self.cleaned_data['group_name'],
            question_pool_type=self.cleaned_data['question_pool_type'],
            initial_members=self.cleaned_data.get('initial_members')
        )
        return group