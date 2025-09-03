from django.shortcuts import render, redirect
from django.db.models import Case, When, IntegerField
from django.db import IntegrityError
from departments.models import Department
from courses.models import Course
from .models import Program, Curriculum
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

    # get list of old course names in this program (to find deleted)
    old_course_names = [course.name for course in program_instance.courses.all()]
    # sooner existing (inputed_names) will be removed from here, so deleted will remain unremoved
    deleted_course_names = old_course_names
    added_course_names = []
    if request.method == 'POST':
        print("=== POST DATA ===")
        for inputName, inputValue in request.POST.items():
            # skip unnecessary input, values
            if(not inputName.startswith('semester_')): continue
            
            # parse semester number
            semester = int(inputName.split('_')[1])

            # get values of all inputs corresponding to semester_{semester}
            input_courses = request.POST.getlist(inputName)

            

            # check existance of inputed course before saving
            for course_name in input_courses:
                # delete from removed inputed course name
                
                if course_name in deleted_course_names: deleted_course_names.remove(course_name)
                course_instance_query = Course.objects.filter(name = course_name)
                
                if course_instance_query.exists():
                    course_instance = course_instance_query.first()
                    #print(f'\033[92mAdding {course_name} to Semester {semester}\033[0m')

                    try:
                        newCurriculumItem = Curriculum(
                            program=program_instance,
                            course=course_instance,
                            numbered_semester=semester
                        )
                        newCurriculumItem.save()
                        
                        # add to added list
                        added_course_names.append(course_name)
                    except IntegrityError:
                        # This is extra safety in case of race conditions
                        # print(f'\033[91mIntegrityError: {course_name} not added (duplicate?)\033[0m')
                        pass
        # delete from table Curriculum deleted_course_names
        for deleted_course_name in deleted_course_names:
            Curriculum.objects.get(
                program=program_instance,
                course= program_instance.courses.get(name = deleted_course_name),
            ).delete()

        print('Deleted Course Names: ', deleted_course_names)
        print('Added Course Names: ', added_course_names)
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
