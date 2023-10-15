from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    pass


class ManagerUserView(generics.RetrieveUpdateAPIView):
    pass
