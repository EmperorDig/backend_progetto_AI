from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser
import pytz


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # La password non deve essere letta

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'password', 'disease_type']

    def validate_birth_date(self, value):
        local_tz = pytz.timezone('Europe/Rome')
        current_date = timezone.now().astimezone(local_tz).date()
        if value > current_date or value < 1900:
            raise serializers.ValidationError("Inserire data di nascita valida")
        return value