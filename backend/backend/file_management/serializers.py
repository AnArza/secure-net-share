from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import File
from ..profiles.serializers import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    shared_with = UserSerializer(many=True, read_only=True)
    class Meta:
        model = File
        fields = ('id', 'file', 'name', 'is_chunked', 'shared_with', 'owner')
        extra_kwargs = {'shared_with': {'required': False}}


class FileShareSerializer(serializers.ModelSerializer):
    shared_with = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username'  # Assuming 'username' is the field you want to use
    )

    class Meta:
        model = File
        fields = ['shared_with']

    def validate(self, attrs):
        shared_with = attrs.get('shared_with', [])
        if not shared_with:
            raise ValidationError('shared_with field cannot be empty.')
        return attrs

    def update(self, instance, validated_data):
        shared_with = validated_data.get('shared_with', [])
        shared_with_users = [User.objects.get(username=shared) for shared in shared_with]
        if shared_with:
            instance.shared_with.set(shared_with_users)  # Set new shared users
        instance.save()
        return instance
