from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        
    # ValidationError - existing name
    def clean_name(self):
        inputed_name = self.cleaned_data.get('name')
        
        if Department.objects.filter(name = inputed_name).exists():
            raise forms.ValidationError('Entered name alrady exists !')

        return inputed_name