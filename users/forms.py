from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from departments.models import Department


from .models import Teacher, Student
class EnrollSysRegistrationForm(forms.Form):
    name = forms.CharField(
        required = False, 
        label = 'First Name',
        widget = forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your first name'})
    )

    surname = forms.CharField(
        required = False,
        label = 'Last Name',
        widget = forms.TextInput(attrs = {'class': 'form-input', 'placeholder': 'Your last name'})
    )

    email = forms.EmailField(
        required = False,
        label = 'Email',
        widget = forms.EmailInput(attrs = {'class': 'form-input' ,'placeholder': 'exampl@email.com'})
    )

    password = forms.CharField(
        required=False,
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
        widget=forms.HiddenInput(),
        required=False
    )
    
    department = forms.ModelChoiceField(
        queryset= Department.objects.all(), 
        required = False,
        label = 'Department'
    )

    #############  ##############

    # -- CUSTOM initialization: --
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # dynamically add user attribute to form
            self.user_instance = user 

            if hasattr(user, 'student'):
                self.fields['role'].initial = 'student'
                self.fields['department'].initial = user.student.department
                print('Editing Student')
            elif hasattr(user, 'teacher'):
                self.fields['role'].initial = 'teacher'
                self.fields['department'].initial = user.teacher.department
                print('Editing Teacher')

            self.fields['name'].initial = user.first_name
            self.fields['surname'].initial = user.last_name
            self.fields['email'].initial = user.email

    # -- CUSTOM VALIDATION: --
    
    # avoid using same email twice.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if hasattr(self, 'user_instance'): same_email = User.objects.all().exclude(pk = self.user_instance.pk).filter(email=email)
        else: same_email =User.objects.all().filter(email=email)
        
        if same_email.exists():
            raise forms.ValidationError('This email is not available !') # user already exists !
        return email
    
    
    def save(self, commit=True, user=None):
        if user is None:  # New user
            user = User(
                username=self.cleaned_data['email'].split('@')[0]
            )

        # Update attributes
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        # ------------------
        # Commit User
        # ------------------
        if commit:
            user.save()

            # ------------------
            # Create/update role objects only if commit=True
            # ------------------
            role = self.cleaned_data['role']

            if role == 'student':
                student, created = Student.objects.get_or_create(
                    user=user,
                    defaults= {'gpa': 0.0, 'department': self.cleaned_data['department']}
                )
                if created:
                    student.gpa = 0.0   
                student.save()

            elif role == 'teacher':
                teacher, created = Teacher.objects.get_or_create(
                    user=user,
                    defaults = {'department': self.cleaned_data['department']}
                )
                teacher.save()

        return user

        