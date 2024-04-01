from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegistrationSerializer,
    # ActivationSerializer,
    # ChangePasswordSerializer,
    # RestorePasswordSerializer,
    # SetRestoredPasswordSerializer,
    )


User = get_user_model()

class RegistrationView(APIView):
    def post(self, request: Request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Thank you for registering! Please activate your account.', 
                status=status.HTTP_201_CREATED
            )


class EmailActivationView(APIView):   
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True       
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated. You can login now.',
            status=status.HTTP_200_OK
            )
  

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Your account has been deleted.',
            status=status.HTTP_204_NO_CONTENT
        )