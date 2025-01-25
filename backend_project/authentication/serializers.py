from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser
import pytz
import re


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


    def validate_password(self, value):
    
        if len(value) < 8:
            raise serializers.ValidationError("La password deve essere lunga almeno 8 caratteri.")

        if not re.search('[A-Z]', value):
            raise serializers.ValidationError("La password deve avere almeno una lettera maiuscola")
        
        if not re.search('[a-z]', value):
            raise serializers.ValidationError("La password deve avere almeno una lettera minuscola")
        
        if not re.search('[0-9]', value):
            raise serializers.ValidationError("La password deve contenere almeno un numero")

        if not re.search('[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.Validationerror("La password deve contenere almeno un carattere speciale")

        return value


    def validate_first_name(self, value):
        
        if not value.isalpha(): #se non sono solo lettere. prima che tu me lo chieda isalpha non è una libreria
            raise serializers.ValidationError("Il nome deve contenere solo lettere.")
        
        value = value[0].upper() + value[1:].lower()
        return value
    

    def validate_last_name(self, value):
        
        if not value.isalpha(): 
            raise serializers.ValidationError("Il cognome deve contenere solo lettere.")
        
        value = value[0].upper() + value[1:].lower()
        return value
