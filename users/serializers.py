# from tokenize import Token
from rest_framework import serializers
from users.models import User, UserProfile
from rest_framework.authtoken.models import Token

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django.contrib.auth import authenticate
from rest_framework import serializers

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     username = serializers.CharField(max_length=255, read_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)

#     def validate(self, data):
#         # The `validate` method is where we make sure that the current
#         # instance of `LoginSerializer` has "valid". In the case of logging a
#         # user in, this means validating that they've provided an email
#         # and password and that this combination matches one of the users in
#         # our database.
#         email = data.get('email', None)
#         password = data.get('password', None)

#         # Raise an exception if an
#         # email is not provided.
#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )

#         # Raise an exception if a
#         # password is not provided.
#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )

#         # The `authenticate` method is provided by Django and handles checking
#         # for a user that matches this email/password combination. Notice how
#         # we pass `email` as the `username` value since in our User
#         # model we set `USERNAME_FIELD` as `email`.
#         user = authenticate(username=email, password=password)

#         # If no user was found matching this email/password combination then
#         # `authenticate` will return `None`. Raise an exception in this case.
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )

#         # Django provides a flag on our `User` model called `is_active`. The
#         # purpose of this flag is to tell us whether the user has been banned
#         # or deactivated. This will almost never be the case, but
#         # it is worth checking. Raise an exception in this case.
#         if not user.is_active:
#             raise serializers.ValidationError(
#                 'This user has been deactivated.'
#             )

#         # The `validate` method should return a dictionary of validated data.
#         # This is the data that is passed to the `create` and `update` methods
#         # that we will see later on.
#         return {
#             'email': user.email,
#             'username': user.username,
#             'token': user.token
#         }

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'profile', 'is_staff')
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
        print(serializer_data)
        username = serializer_data.get('username')
        is_staff = serializer_data.get('is_staff')
        # is_student = serializer_data.get('is_student')
        # is_teacher = serializer_data.get('is_teacher')
        return {
            'is_staff': is_staff,
            'username': username,
            # 'is_student': is_student,
            # 'is_teacher': is_teacher
        }