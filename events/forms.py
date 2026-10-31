from django import forms
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from accounts.models import UserProfile

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'date',
            'time',
            'end_time',
            'venue',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                self.add_error(
                    'end_time',
                    'End time must be later than the start time.'
                )
        return cleaned_data

        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    onboarding_preference = forms.ChoiceField(
        choices=UserProfile.ONBOARDING_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]