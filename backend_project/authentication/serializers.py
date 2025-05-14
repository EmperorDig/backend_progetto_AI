from django.utils import timezone
from rest_framework import serializers
from .models import PatientUser, DoctorUser
import datetime
import pytz
import re
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)  # La password non deve essere letta
    birth_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y'])
    MIN_BIRTH_DATE = datetime.date(1900, 1, 1)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'birth_date', 'password']
    def validate_birth_date(self, value):
        local_tz = pytz.timezone('Europe/Rome')
        today = timezone.now().astimezone(local_tz).date()
        if not (today >= value >= self.MIN_BIRTH_DATE):
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
            raise serializers.ValidationError("La password deve contenere almeno un carattere speciale")
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


class DoctorUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = DoctorUser
        fields = UserSerializer.Meta.fields


class PatientUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PatientUser
        fields = UserSerializer.Meta.fields + ['disease_type']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
