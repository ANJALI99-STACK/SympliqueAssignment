from rest_framework import serializers
from .models import Reminder
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReminderSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    remind_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ['remind_at']
    
    def validate(self, data):
        """
        Validate the data and combine date and time into remind_at.
        """
        date = data.get('date')
        time = data.get('time')
        
        if not date or not time:
            raise serializers.ValidationError("Both date and time are required.")

        # Create a naive datetime by combining date and time
        naive_datetime = datetime.combine(date, time)
        
        # Make it timezone-aware explicitly using Django's timezone utility
        remind_at = timezone.make_aware(naive_datetime)
        
        # Log to verify it's timezone-aware
        logger.info(f"remind_at in validate: {remind_at}, is_aware: {timezone.is_aware(remind_at)}")
            
        # Ensure reminder time is in the future
        if remind_at <= timezone.now():
            raise serializers.ValidationError("Reminder time must be in the future.")

        # Add remind_at to the validated data
        data['remind_at'] = remind_at
        return data
        
    def create(self, validated_data):
        """
        Create and return a new Reminder instance.
        Ensure remind_at is timezone-aware before saving.
        """
        # Extract remind_at from validated data
        remind_at = validated_data.get('remind_at')
        
        # Double-check timezone awareness
        if remind_at and not timezone.is_aware(remind_at):
            validated_data['remind_at'] = timezone.make_aware(remind_at)
            logger.warning("Had to make remind_at timezone-aware in create method")
        
        # Create the instance
        instance = Reminder.objects.create(**validated_data)
        
        # Log after creation
        logger.info(f"Created reminder with remind_at: {instance.remind_at}, is_aware: {timezone.is_aware(instance.remind_at)}")
        
        return instance