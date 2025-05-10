from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReminderSerializer
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ReminderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReminderSerializer(data=request.data)

        if serializer.is_valid():
            # Log validated data
            logger.info(f"Validated data: {serializer.validated_data}")
            
            # Check reminder_at timezone awareness before saving
            if 'remind_at' in serializer.validated_data:
                remind_at = serializer.validated_data['remind_at']
                logger.info(f"remind_at before save: {remind_at}, is_aware: {timezone.is_aware(remind_at)}")
            
            # Save the reminder to the database
            reminder = serializer.save()
            
            # Check the saved instance
            logger.info(f"Saved reminder remind_at: {reminder.remind_at}, is_aware: {timezone.is_aware(reminder.remind_at)}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)