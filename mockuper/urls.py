from django.urls import path
from mockuper import views


urlpatterns = [
    path('mockups/generate/', 
        views.generate_mockup_shirt, name='generate-mockup-shirt'),
    path('tasks/<uuid:task_uuid>/', 
        views.get_task_status, name='get-task-status-detail'),
    path('mockups/', 
        views.mockups_history, name='mockups-history'),
]
