from rest_framework import serializers
from .models import Audio
from mutagen import File

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

    def validate(self, data):
        audio_file = data.get('audio_file')
        if audio_file:
            audio_file.seek(0)  # Ensure we're reading from the start of the file
            audio = File(audio_file)
            if audio is not None:
                data['length'] = audio.info.length  # Length in seconds
        return data