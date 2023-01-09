from rest_framework import serializers
from users.models import User, UserProfile
from rest_framework.authtoken.models import Token

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True, allow_blank=True)
#     password = serializers.CharField(style={'input_type': 'password'})

#     class Meta:
#         model = User
#         fields = ( 'username', 'password')

#     # def authenticate(email, password):
#     #     try:
#     #         user = User.objects.get(email=email)
#     #         print(user)
#     #         if user.check_password(password):
#     #             return user
#     #     except User.DoesNotExist:
#     #         pass
#     #     return None
    
#     def validate(self, data):
#         print(data)
#         user = authenticate(username=data['username'], password=data['password'])
#         print (f"The user is: {user}")
#         if user is None:
#             raise serializers.ValidationError('Invalid Login Credentials')
#         return user
    
    



class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance

class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = '__all__' 

    def get_user_type(self, obj):
        serializer_data = UserSerializer(obj.user, context=serializer_context).data
        # is_staff = serializer_data.get('is_staff')
        # is_student = serializer_data.get('is_student')
        # is_teacher = serializer_data.get('is_teacher')
        # return {
        #     'is_student': is_student,
        #     'is_teacher': is_teacher
        # }