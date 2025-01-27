from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser
import datetime
import pytz

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # La password non deve essere letta
    birth_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y'])

    MIN_BIRTH_DATE = datetime.date(1900, 1, 1)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'password', 'disease_type']

    def validate_birth_date(self, value):
        local_tz = pytz.timezone('Europe/Rome')
        today = timezone.now().astimezone(local_tz).date()
        if not (today >= value >= self.MIN_BIRTH_DATE):
            raise serializers.ValidationError("Inserire data di nascita valida")
        return value

