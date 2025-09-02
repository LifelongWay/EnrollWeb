from django.shortcuts import render, redirect
from django.db.models import Case, When, IntegerField
from departments.models import Department
from .models import Program
from .forms import ProgramNameForm



# Create your views here.
def curriculums_editor(request):
    context = {}
    context['departments'] = Department.objects.all()

    return render(request, 'curriculums/curriculum_editor.html', context)

def curriculum_add(request, dept_id):
    context = {}
    context['departments'] = makefirst(Department.objects.all(), dept_id)
    
    department_modifying = Department.objects.all().get(pk = dept_id)
    
    if request.method == 'POST':
        program_form = ProgramNameForm(request.POST)
        if program_form.is_valid():
            print('SDF')
            program_instance = program_form.save(commit = False)
            program_instance.department = department_modifying
            program_instance.save()
        else:
            print('Program Form Errors')
            print(program_form.errors)
        
        return redirect('curriculums:editor')
    else:
        context['program_form'] = ProgramNameForm()
        context['editing_department_id'] = dept_id

    
    return render(request, 'curriculums/curriculum_editor.html', context)


def curriculum_edit(request, program_id):
    context = {}
    
    context['departments'] = Department.objects.all()
    context['editing_program_id'] = program_id
    program_instance = Program.objects.all().get(pk = program_id)
    editing_department_id = program_instance.department.pk
    context['departments'] = makefirst(context['departments'], editing_department_id)


    if request.method == 'POST':
        program_form = ProgramNameForm(request.POST)
        if program_form.is_valid():
            pass
        else:
            print('Program Form Errors')
            print(program_form.errors)
        
        return redirect('curriculums:editor')
    else:
        context['program_form'] = ProgramNameForm(instance = program_instance)
        

    return render(request, 'curriculums/curriculum_editor.html', context)

def curriculum_delete(request, program_id):
    pass

def my_curriculum(request):
    pass



def makefirst(object_list, pk):
    # handle variable not defined
    if not pk:
        return object_list
    # making object of pk = pk first
    return object_list.annotate(
        first = Case(
            When(pk = pk, then = 1),
            default = 0,
            output_field=IntegerField()
        )
    ).order_by('-first')
