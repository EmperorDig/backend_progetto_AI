from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Gioco, Partita, Proprieta, ValoreProprietaPartita
from .serializers import (
    GiocoSerializer,
    PartitaSerializer,
    ProprietaSerializer,
    ValoreProprietaPartitaSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def MatchCreate(request):
    serializer = PartitaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def MatchList(request):
    partite = Partita.objects.all()
    serializer = PartitaSerializer(partite, many=True)
    return Response(serializer.data)

def AssignPropertyValue(request):
    serializer = ValoreProprietaPartitaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

