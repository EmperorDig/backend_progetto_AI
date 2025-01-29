from rest_framework import serializers
from .models import Audio, AudioData
from pydub import AudioSegment
import platform
import os

# Determina il sistema operativo
system = platform.system()
print(system)

if system == 'Windows':
    ffmpeg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffmpeg.exe')  # Per Windows
    ffprobe_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffprobe.exe')  # Per Windows
elif system == 'Linux':
    ffmpeg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffmpeg')  # Per Linux
    ffprobe_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffprobe')  # Per Linux
else:
    raise Exception("Sistema operativo non supportato.")

os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
os.environ["PATH"] += os.pathsep + os.path.dirname(ffprobe_path)

try:
    AudioSegment.ffmpeg = ffmpeg_path
    AudioSegment.ffprobe = ffprobe_path
except Exception as e:
    print(f"Errore durante il caricamento di ffmppeg: {e}")




#SERIALIZERS



class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

    def validate(self, data):
        audio_file = data.get('audio_file')
        if audio_file:
            audio_file.seek(0)  # Ensure we're reading from the start of the file
            try:
                audio = AudioSegment.from_file(audio_file)
                if audio is not None:
                    data['length'] = len(audio) / 1000.0  # Length in seconds
            except Exception as e:
                raise serializers.ValidationError(f"Errore durante la lettura del file audio: {e}")
        else:
            raise serializers.ValidationError("Nessun file audio fornito.")
        return data
    

class AudioDataSerializer(serializers.ModelSerializer):

    stutter_percentage = serializers.FloatField(allow_null=True, required=False)
    word_matches = serializers.ListField(child=serializers.CharField(), allow_null=True, required=False)
    syllable_matches = serializers.ListField(child=serializers.CharField(), allow_null=True, required=False)
    letter_matches = serializers.ListField(child=serializers.CharField(), allow_null=True, required=False)

    class Meta:
        model = AudioData
        fields = '__all__'
