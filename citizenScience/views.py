from rest_framework import viewsets
from .models import Disaster
from .serializers import DisasterSerializer
from users.permissions import IsLoggedInUserOrAdmin, IsAdminUser

from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
import requests

class DisasterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsLoggedInUserOrAdmin,)
    queryset = Disaster.objects.all()
    serializer_class = DisasterSerializer


@login_required
def google_login(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        print(access_token)

        # Validate the access token with Google
        google_response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', params={'access_token': access_token})
        google_data = google_response.json()

        if 'error_description' in google_data:
            return JsonResponse({'error': 'Invalid access token'})

        # Check if the user is already associated with a SocialAccount
        social_account = SocialAccount.objects.filter(uid=google_data['sub'], provider='google').first()

        if social_account:
            # Existing user, log them in
            user = social_account.user
        else:
            # Create a new user
            user = request.user  # Use the current user or create a new one

            # Associate the SocialAccount with the user
            social_account = SocialAccount.objects.create(user=user, provider='google', uid=google_data['sub'])

        # Save additional user data
        first_name = google_data.get('givenName', '')
        last_name = google_data.get('familyName', '')
        username = first_name + last_name
        user.username = username
        user.email = google_data.get('email', '')
        user.save()

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