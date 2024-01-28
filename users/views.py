from rest_framework import viewsets

from users.models import User, UserProfile
from users.serializers import UserSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from users.permissions import IsLoggedInUserOrAdmin, IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
   permission_classes = (IsLoggedInUserOrAdmin,)
   queryset = User.objects.all()
   serializer_class = UserSerializer

    
       # Add this code block
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class UserProfileViewSet(viewsets.ModelViewSet):
   permission_classes = (IsLoggedInUserOrAdmin,)

   queryset = UserProfile.objects.all()
   serializer_class = UserProfileSerializer
       # Add this code block
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data.get('user', {})

#         # Notice here that we do not call `serializer.save()` like we did for
#         # the registration endpoint. This is because we don't  have
#         # anything to save. Instead, the `validate` method on our serializer
#         # handles everything we need.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)