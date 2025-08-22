from django import forms
from .models import Course, Section

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['department', 'name', 'credits', 'prerequisite_courses']

        widgets = {
            'department': forms.Select(
                attrs={
                    'class': 'form-select shadow-sm rounded-3',
                    'style': 'max-width:400px;'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control shadow-sm rounded-3',
                    'placeholder': 'Enter course name',
                    'style': 'max-width:400px;'
                }
            ),
            'credits': forms.NumberInput(
                attrs={
                    'class': 'form-control shadow-sm rounded-3',
                    'placeholder': 'e.g. 3',
                    'style': 'max-width:200px;'
                }
            ),
            'prerequisite_courses': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'form-check-list shadow-sm rounded-3 p-2',
                }
            )
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['teacher', 'image', 'section_number', 'course', 'capacity', 'year', 'semester', 'students']

        labels = {
            'teacher': 'Instructor',
            'image': 'Image (',
            'section_number': 'SECTION.NO:',
            'course': 'Course',
            'capacity': 'Class Capacity:',
        }