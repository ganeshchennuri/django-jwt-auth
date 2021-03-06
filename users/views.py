from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt
import datetime


class RegisterView(APIView):
    """Api View for User Registration"""
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response (serializer.data)
 
class LoginView(APIView):
    """"Api View for Login"""
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User Does Not Exists")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload,"secret",algorithm="HS256")
        #.decode("utf-8")
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            "message": " success",
            "token": token
        }
        
        return response


class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("User is not Authenticated")
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token Expired")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
   
        return response