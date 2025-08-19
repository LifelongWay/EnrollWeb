from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class EnrollSysRegistrationForm(UserCreationForm):
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

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Minimum 8 chars!'


    # CUSTOM VALIDATION: 
     
    # avoid using same email twice.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('This email is not available !') # user already exists !
        return email
    
    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user