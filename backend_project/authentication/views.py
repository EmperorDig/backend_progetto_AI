from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = CustomUser.objects.create_user(**serializer.validated_data)
        print(f"New user registered: {user.email}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
potrebbe essere inutile

@api_view(['GET'])
@permission_classes([AllowAny])
def LoginUser(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = CustomUser.objects.get(email=email)
        if user.check_password(password):
            return Response({'token': user.token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
"""

@api_view(['GET'])
def ListUsers(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VIstaProtetta(request):
    return Response({'message': 'Questa è una vista protetta!'})
