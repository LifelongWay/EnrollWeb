from django.urls import path
from .views import courses_and_sections_view
from django.conf import settings 
from django.conf.urls.static import static
app_name = 'courses'

urlpatterns = [
    path('panel/', courses_and_sections_view, name = 'panel') # management panel - should be secured
]
