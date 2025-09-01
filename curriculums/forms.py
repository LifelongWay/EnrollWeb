from django import forms
from .models import Program

class ProgramNameForm(forms.ModelForm):
    
    class Meta():
        model = Program
        fields = ['name', 'degree']

        widgets = {
            'name': forms.TextInput(),
            'degree': forms.Select(),
        }
