from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class meta:
        model=UserProfile
        fields='__all__'

