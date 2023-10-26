from django.contrib.auth import login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, UserSerializer, PasswordResetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .email_utils import send_password_reset_email


# email settings
from django.conf import settings
from django.core.mail import send_mail



# registration endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Token.objects.create(user=user)

            subject = 'welcome to GFG world'
            message = f'Hi {user.firstname}, thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
# html_message
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# user login endpoint
@api_view(['POST'])
def user_login(request):
    user = User.objects.filter(email=request.data['email'], password=request.data['password']).first()
    
    if user:
        data = user.firstname + ' ' + user.lastname

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_password_reset_link(request):
    if request.method == 'POST':
        email = request.data.get('email')  
        reset_link = generate_reset_link(email) 
        send_password_reset_email(email, reset_link)
        return Response({'message': 'Password reset email sent successfully'})

# user logout endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Get the user's authentication token
    token, created = Token.objects.get_or_create(user=request.user)
    
    token.delete()
    
    return Response({'message': 'You are now logged out.'})

