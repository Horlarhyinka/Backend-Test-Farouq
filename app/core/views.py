from rest_framework import generics
from .models import User, UserManager
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from datetime import datetime

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        data = {"email": request.data.get("email"), "password": request.data.get("password")}
        print(data)
        if not data["email"] or not data["password"]:
            return Response({"message": "email and password is required", status: status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response({"message": "user not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
        if user.password != data["password"]:
            return Response({"message": "Incorrect password", "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            serialized = UserSerializer(user)
            user.last_login = datetime.now()
            User.objects.filter(email=data["email"]).update(last_login=datetime.now())
            return Response({"user":serialized.data, "token": { "access": str(access), "refresh": str(refresh)}}, status=status.HTTP_200_OK)
        except Exception as err:
            print(f"error occured: {err}")
            return Response({"message": "internal server error", "details": err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
