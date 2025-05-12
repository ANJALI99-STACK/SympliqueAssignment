from django.urls import path
from .views import ReminderCreateView, home

urlpatterns = [
    path('', home, name='home'),  # Simple homepage for /
    path('reminders/', ReminderCreateView.as_view(), name='create_reminder'),
]
