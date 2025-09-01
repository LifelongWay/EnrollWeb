from django.urls import path
from . import views

app_name = 'curriculums'

urlpatterns = [
    path('my/', views.my_curriculum, name = 'my'),
    path('programs/', views.curriculums_editor, name = 'editor'),
    path('programs/add/<int:dept_id>/', views.curriculum_add, name = 'program-add'),
    path('programs/edit/<int:program_id>/', views.curriculum_edit, name = 'program-edit'),
    path('programs/edit/<int:program_id>/', views.curriculum_delete, name = 'program-delete'),
]
