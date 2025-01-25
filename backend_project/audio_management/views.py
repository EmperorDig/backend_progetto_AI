from rest_framework import status
from .models import Audio
from .serializers import AudioSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def AudioListView(request):
    queryset = Audio.objects.all()
    serializer = AudioSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def AudioCreateView(request):
    serializer = AudioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)