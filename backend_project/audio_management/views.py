from rest_framework import generics
from .models import Audio
from .serializers import AudioSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def AudioListCreateView(request):
    queryset = Audio.objects.all()
    serializer = AudioSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def AudioCreateView(request):
    serializer = AudioSerializer(data=request.data)
    if serializer.is_valid():
        audio_instance = serializer.save()
        audio_instance.save()  # This will trigger the save method in the model to calculate the length
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)