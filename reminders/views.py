from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReminderSerializer
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ReminderCreateView(APIView):
    """
    API view to create a new reminder.
    Logs data and checks timezone awareness of the remind_at field.
    """

    def post(self, request, *args, **kwargs):
        serializer = ReminderSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(f"Invalid reminder data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        logger.info(f"Validated data: {validated_data}")

        remind_at = validated_data.get('remind_at')
        if remind_at:
            logger.info(f"remind_at (pre-save): {remind_at} | Timezone aware: {timezone.is_aware(remind_at)}")

        reminder = serializer.save()

        logger.info(f"Saved reminder ID: {reminder.id} | remind_at (post-save): {reminder.remind_at} | Timezone aware: {timezone.is_aware(reminder.remind_at)}")

        return Response(ReminderSerializer(reminder).data, status=status.HTTP_201_CREATED)
