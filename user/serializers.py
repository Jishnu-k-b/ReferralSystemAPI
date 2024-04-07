from rest_framework import serializers
from .models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "referral_code",
            "my_referral_code",
            "created_at",
        ]


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = "__all__"
