from django.urls import path
from . import views

app_name = 'curriculums'

urlpatterns = [
    path('my/', views.my_program, name = 'my'),
    path('programs/', views.curriculums_editor, name = 'editor'),
    path('programs/add/<int:dept_id>/', views.program_add, name = 'program-add'),
    path('programs/edit/<int:program_id>/', views.program_edit, name = 'program-edit'),
    path('programs/edit/<int:program_id>/', views.program_delete, name = 'program-delete'),
]
