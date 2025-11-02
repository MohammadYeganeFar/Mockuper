from django.urls import path
from mockuper import views


urlpatterns = [
    path('mockups/generate/', 
        views.generate_mockup_shirt, name='generate-mockup-shirt'),
]
