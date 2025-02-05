from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PatientUser, DoctorUser

class IsAuthenticatedPatientUser(BasePermission):
    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        user, validated_token = jwt_authenticator.authenticate(request)
        
        return user and user.is_authenticated and PatientUser.objects.filter(email=user.email).exists()

class IsAuthenticatedDoctorUser(BasePermission):
    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        user, validated_token = jwt_authenticator.authenticate(request)
        
        return user and user.is_authenticated and DoctorUser.objects.filter(email=user.email).exists()