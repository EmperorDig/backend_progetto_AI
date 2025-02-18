from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Audio
from .serializers import AudioSerializer, AudioDataSerializer
from .riconoscimento_balbuzia import process_audio_file
from authentication.permissions import IsAuthenticatedPatientUser, IsAuthenticatedDoctorUser

@api_view(['GET'])
def PingView(request):
    return Response("ciao")

@api_view(['GET'])
@permission_classes([IsAuthenticatedDoctorUser])
def AudioListView(request):
    queryset = Audio.objects.all()
    serializer = AudioSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedPatientUser])
def AudioCreateView(request):
    serializer = AudioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAudioData(request, audio_id):
    audio = get_object_or_404(Audio, id=audio_id)
    file_path = audio.audio_file.path

    if audio.audio_data:
        data = {
            "stutter_percentage" : audio.audio_data.stutter_percentage,
            "word_matches" : audio.audio_data.word_matches,
            "syllable_matches" : audio.audio_data.syllable_matches,
            "letter_matches" : audio.audio_data.letter_matches
        }
        serializer = AudioDataSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
    return Response(AnalyzeAudio(file_path, audio))

def AnalyzeAudio(file_path, audio):
    data = process_audio_file(file_path)

    serializer = AudioDataSerializer(data=data)
    if serializer.is_valid():
        audio_data = serializer.save()  # Salva il nuovo AudioData
        audio.audio_data = audio_data  # Assegna l'oggetto AudioData all'Audio
        audio.save()  # Salva le modifiche
        return serializer.data

    return serializer.errors
