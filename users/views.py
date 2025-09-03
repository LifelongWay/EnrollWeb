from django.shortcuts import render, redirect
from .forms import EnrollSysRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import logout, login, authenticate
from .models import Student, Teacher
from curriculums.models import Program

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


# show management panel for given role [REGISTRAR-ONLY]
def roles_view(request, role):
    context = {}
    context['role'] = role
    if role == 'student':
        context['students'] = Student.objects.all()
    elif role == 'teacher':
        context['teachers'] = Teacher.objects.all()
    return render(request, 'users/registrar/user_panel.html', context)

def account_add_view(request, role):
    context = {}
    context['role'] = role

    if role == 'student':
        context['students'] = Student.objects.all()
    elif role == 'teacher':
        context['teachers'] = Teacher.objects.all()
    context['form'] = EnrollSysRegistrationForm(initial = {'role': role})

    if request.method == 'POST':
        form = EnrollSysRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:panel', role=role)
        else:
            print(form.errors)
    return render(request, 'users/registrar/user_panel.html', context)


# Profile page [COMMON]
def profile_view(request, user_id):
    user = User.objects.get(pk = user_id)
    context = {'user_viewed': user}
    return render(request, 'users/profile.html', context)


def profile_edit_view(request, user_id):
    user_under_edit = User.objects.get(pk = user_id)
    context = {'user_viewed': user_under_edit}

    form = EnrollSysRegistrationForm(user=user_under_edit)
    context['form'] = form

    if request.method == 'POST':
        # check for program change
        if hasattr(user_under_edit, 'student'):
            if(request.POST.get('program')):
                print('Program: ', request.POST.get('program'))
                updated_program = Program.objects.get(name = request.POST.get('program'))
                user_under_edit.student.program = updated_program
                user_under_edit.student.save()
                print('Saved Program!')
                
        # other attrib-s.
        form = EnrollSysRegistrationForm(request.POST, request.FILES ,user=user_under_edit)
        context['form'] = form

        if form.is_valid():
            form.save(user=user_under_edit)
            
            return redirect('users:profile', user_id=user_id)
        else:
            print(form.errors)

    # if editing student, pass programs of department
    if hasattr(user_under_edit, 'student'):
        context['programs'] = Program.objects.filter(department = user_under_edit.student.department)
    
    return render(request, 'users/profile.html', context)