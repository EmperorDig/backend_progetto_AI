from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer

@api_view(['POST'])
def RegisterUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = CustomUser.objects.create_user(**serializer.validated_data)
        print(f"New user registered: {user.email}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ListUsers(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
