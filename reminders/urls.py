from django.urls import path
from .views import ReminderCreateView

urlpatterns = [
    path('reminders/', ReminderCreateView.as_view(), name='create_reminder'),
]
