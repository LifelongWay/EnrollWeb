from django.shortcuts import render
from .models import Department

# Create your views here.
def departments_view(request):
    context = {}
    departments = Department.objects.all()

    context['departments'] = departments
    return render(request, 'departments/departments_panel.html', context)