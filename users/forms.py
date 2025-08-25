from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from departments.models import Department

from .models import Teacher, Student
class EnrollSysRegistrationForm(forms.Form):
    name = forms.CharField(
        required = True, 
        label = 'First Name',
        widget = forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your first name'})
    )

    surname = forms.CharField(
        required = True,
        label = 'Last Name',
        widget = forms.TextInput(attrs = {'class': 'form-input', 'placeholder': 'Your last name'})
    )

    email = forms.EmailField(
        required = True,
        label = 'Email',
        widget = forms.EmailInput(attrs = {'class': 'form-input' ,'placeholder': 'exampl@email.com'})
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )

    ## used by Registrars ONLY ##
    ROLE_CHOICES = [
            ('teacher', 'Teacher'),
            ('student', 'Student'),
    ]

    role = forms.ChoiceField(
        choices = ROLE_CHOICES,
        label = 'Role',
        widget=forms.HiddenInput()
    )
    
    department = forms.ModelChoiceField(
        queryset= Department.objects.all(), 
        required = True,
        label = 'Department'
    )

    #############  ##############

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    # CUSTOM VALIDATION: 
     
    # avoid using same email twice.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('This email is not available !') # user already exists !
        return email
    
    
    def save(self, commit = True):
        # Init User instance
        user = User(
            first_name = self.cleaned_data['name'],
            last_name = self.cleaned_data['surname'],
            username = self.cleaned_data['email'].split('@')[0], 
        )
        user.set_password(self.cleaned_data['password'])


        if commit:
            user.save()
            
            # Create related Student/Teacher account after creating User
            if self.cleaned_data.get('role') == 'student':
                Student.objects.create(
                    user = user,
                    gpa = 0.0,
                    department = self.cleaned_data['department']
                )
            elif self.cleaned_data.get('role') == 'teacher':
                Teacher.objects.create(
                    user = user, 
                    department = self.cleaned_data['department']
                )
            else:
                print('!! EMPTY USER CREATED !!')
        
        return user
    