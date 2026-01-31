from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['valeur']
        widgets = {
            'valeur': forms.NumberInput(attrs={
                'min': 0,
                'max': 5
            })
        }