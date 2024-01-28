from rest_framework import viewsets
from .models import Disaster
from users.models import User
from .serializers import DisasterSerializer
from users.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from django.http import JsonResponse
import requests
import json

provider = 'google'
social_app = SocialApp.objects.get(provider=provider)
now = timezone.now()

class DisasterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsLoggedInUserOrAdmin,)
    queryset = Disaster.objects.all()
    serializer_class = DisasterSerializer



def google_login(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        access_token = data.get('access_token')
        expires_in = data.get('expires_at')
        email = data.get('email')
        expires_at = now + timedelta(seconds=expires_in)
        print(access_token)

        # Check if the token already exists in SocialToken
        user = User.objects.filter(email=email).first()

        if user:
            # Token already exists, return the existing token information
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'access_token': access_token,
            })

        # Validate the access token with Google
        google_response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', params={'access_token': access_token})
        google_data = google_response.json()
        print(google_data)
        if 'error_description' in google_data:
            return JsonResponse({'error': 'Invalid access token'})

        # Check if the user is already associated with a SocialAccount
        social_account = SocialAccount.objects.filter(uid=google_data['sub'], provider='google').first()

        if request.user.is_authenticated:
            user = request.user
        else:
            # Create a new user
            user = User.objects.create_user(username=google_data.get('email', ''),
                                            email=google_data.get('email', ''),
                                            password=make_password(None),
                                            )

        # Associate the SocialAccount with the user
        social_account = SocialAccount.objects.create(user=user, provider='google', uid=google_data['sub'])

        # Save additional user data
        first_name = google_data.get('given_name', '')
        last_name = google_data.get('family_name', '')
        username = first_name + last_name
        user.username = username
        user.email = google_data.get('email', '')
        user.save()

        social_token, _ = SocialToken.objects.get_or_create(
            account=social_account, token=access_token,
            app=social_app,
            expires_at=expires_at
        )

        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access_token': access_token,
        })
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
