from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from backend.profiles.models import UserProfile
from .serializers import UserRegistrationSerializer, UserProfileSerializer


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return Response(UserProfileSerializer(user_profile).data)


class UserLoginAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        user_profile = UserProfile.objects.get(user=user)
        # Update user's online status to True when logged in
        user_profile.is_online = True
        user_profile.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "active_users",
            {
                "type": "user.status.change",
                "message": {
                    "user_id": user.id,
                    "status": "online"
                }
            }
        )

        return response

class UserLogoutAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        # Update user's online status to False when logged out
        user_profile.is_online = False
        user_profile.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "active_users",
            {
                "type": "user.status.change",  # This should match the method in your consumer
            }
        )

        for file_id in request.user.files.values_list('id', flat=True):
            async_to_sync(channel_layer.group_send)(
                "file_updates",
                {
                    "type": "file_deleted",
                    "file_id": file_id
                }
            )

        request.user.files.all().delete()

        return Response(status=status.HTTP_200_OK)

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class ActiveUserListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve a queryset of active users based on login records
        active_users = UserProfile.objects.filter(is_online=True).exclude(user=self.request.user)
        return active_users