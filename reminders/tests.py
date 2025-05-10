from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Reminder

class ReminderAPITest(TestCase):
    """Test suite for the Reminder API"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = APIClient()
        self.url = reverse('create_reminder')
        
        # Use timezone.now() to get timezone-aware datetime
        tomorrow = timezone.now() + timedelta(days=1)
        self.valid_payload = {
            "message": "Test reminder",
            "date": tomorrow.date().isoformat(),
            "time": "10:00:00",
            "reminder_type": "email"
        }

    def tearDown(self):
        """Clean up after tests"""
        Reminder.objects.all().delete()

    def test_create_valid_reminder(self):
        """Test creating a valid reminder returns 201 Created"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("remind_at", response.data)
        
        # Verify the reminder was actually created in the database
        self.assertEqual(Reminder.objects.count(), 1)
        reminder = Reminder.objects.first()
        self.assertEqual(reminder.message, self.valid_payload["message"])
        self.assertTrue(timezone.is_aware(reminder.remind_at))  # Check that datetime is timezone-aware

    def test_missing_field(self):
        """Test that missing required fields return 400 Bad Request"""
        invalid_payload = self.valid_payload.copy()
        del invalid_payload["date"]
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        
        # Verify no reminder was created
        self.assertEqual(Reminder.objects.count(), 0)

    def test_reminder_in_past(self):
        """Test that reminders in the past are rejected"""
        past_payload = self.valid_payload.copy()
        yesterday = timezone.now() - timedelta(days=1)
        past_payload["date"] = yesterday.date().isoformat()
        response = self.client.post(self.url, past_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Reminder time must be in the future", str(response.data))
        
        # Verify no reminder was created
        self.assertEqual(Reminder.objects.count(), 0)