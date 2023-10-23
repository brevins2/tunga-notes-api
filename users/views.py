from django.contrib.auth import login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, UserSerializer, PasswordResetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


# registration endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.get_or_create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user login endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful, welcome to Tunga notes app'})
        return Response({'message': 'Login failed, invalid credentails. Please try again!'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# password reset endpoint
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def password_reset(request):
#     serializer = PasswordResetSerializer(data=request.data)
#     if serializer.is_valid():
#         Implement email reset logic here, send a reset link
#         return Response({'message': 'Password reset link sent'})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            return Response('user found')
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
        # Generate a password reset token
        # token = default_token_generator.make_token(user)
            
        # Create a password reset link and send it via email
        # current_site = get_current_site(request)
        # mail_subject = 'Password Reset'
        # message = render_to_string('reset_password_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': token,
        # })
        # email = EmailMessage(mail_subject, message, to=[email])
        # email.send()
            
        # return Response({'message': 'Password reset link sent'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user logout endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Get the user's authentication token
    token, created = Token.objects.get_or_create(user=request.user)
    
    token.delete()
    
    return Response({'message': 'You are now logged out.'})
