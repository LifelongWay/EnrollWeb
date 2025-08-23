from django.shortcuts import render, redirect
from .models import Department
from .forms import DepartmentForm

# Create your views here.
def departments_view(request):
    context = {}
    departments = Department.objects.all()

    context['departments'] = departments
    return render(request, 'departments/departments_panel.html', context)

def departments_add_view(request):
    context = {}
    departments = Department.objects.all()
    context['departments'] = departments

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments:panel')
        else:
            print('Denied !')        
    else:
        form = DepartmentForm()
    context['form'] = form
    
    return render(request, 'departments/departments_panel.html', context)