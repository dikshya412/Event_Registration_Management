from django import forms 
from .models import OrganizerRequest

class OrganizerRequestForm(forms.ModelForm):

    class Meta:
        model = OrganizerRequest
        fields = ['reason']

        widgets = {
            'reason':forms.Textarea(attrs={
                'rows':5,
                'placeholder':'Explain why you want to become an event organizer...'
            })
        }
        labels = {
            'reason':'why do you want to become an organizer?'
        }