from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view
from .serializers import LoginSerializer
from .models import User
import jwt

# Create your views here.

# Simple Authentication with Django Templates

def user_login(request):
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def submit_login(request):
   if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Invalid user or password.')
        return redirect('/')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')


# Authentication with JWT (Json Web Token) and API's with Django Rest Framework
    
@api_view(['GET'])
def jwt_user_view(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return Response({'message': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return Response({'message': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)

    user = User.objects.get(username=payload['username'])
    serializer = LoginSerializer(user)

    return Response(serializer.data)
  
@api_view(['POST'])
def jwt_user_login(request):
    if request.data:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            exp = datetime.utcnow() + timedelta(hours=1)
            iat = datetime.utcnow()
            
            payload ={
                'username':username, 
                'password':password, 
                'exp': exp,
                'iat': iat,
            }   
            token = jwt.encode(payload, 'secret', algorithm='HS256')    

            data = {
                'jwt': token,
            } 
            response = Response() 
            response.data = data
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.status_code = HTTP_200_OK

            return response
        else:
            return Response({'message': 'Invalid user or passwaord!'}, status=HTTP_401_UNAUTHORIZED)

@api_view(['POST', 'GET'])
def jwt_user_logout(request):
    response = Response()
    response.delete_cookie('jwt')

    response.data = {
        'message': 'sucess'
    }
    return response