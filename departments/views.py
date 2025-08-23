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

def departments_edit_view(request, dept_id):
    context = {}
    departments = Department.objects.all()
    
    context['departments'] = departments
    context['editing_dept_id'] = dept_id
    department_to_edit = departments.get(dept_id = dept_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance = department_to_edit)
        if form.is_valid():
            form.save()
            return redirect('departments:panel')
    
    print('dpt edt: ', department_to_edit)
    form = DepartmentForm(instance = department_to_edit)
    context['form'] = form

    return render(request, 'departments/departments_panel.html', context)

def departments_delete_view(request, dept_id):
    deleting_department = Department.objects.get(dept_id = dept_id)
    deleting_department.delete()
    return redirect('departments:panel')