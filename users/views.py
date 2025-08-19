from django.shortcuts import render, redirect
from .forms import EnrollSysRegistrationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group

# Create your views here.
def login_view(request):  # Renamed from 'login'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Using renamed import
                return redirect('/')
        # Add this to see errors in console for debugging
        print("Form errors:", form.errors)  
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/auth/login.html', context)  # Changed to login.html


def register(request):
    if request.method == 'POST':
        form = EnrollSysRegistrationForm(request.POST)
        if form.is_valid():
            # save user in model
            user = form.save()
            
            # automatically add to Student group
            student_group, is_first_student = Group.objects.get_or_create(name = "Student")
            user.groups.add(student_group)
            
            if is_first_student:
                print('\033[92mFirst student created!\033[0m')

            # automatically login after registering user
            login(request, user)
            return redirect('/')
    else:
        form = EnrollSysRegistrationForm()


    context = {
        'form': form
    }
    return render(request, 'users/auth/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')