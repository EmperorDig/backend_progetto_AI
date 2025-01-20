from rest_framework import serializers
from .models import AudioFile

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'