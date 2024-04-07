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
        extra_kwargs = {
            "email": {
                "required": True,
                "error_messages": {"required": "This field is required."},
            },
            "first_name": {
                "required": True,
                "error_messages": {"required": "This field is required."},
            },
            "last_name": {
                "required": True,
                "error_messages": {"required": "This field is required."},
            },
            "referral_code": {"required": False},
            "my_referral_code": {"required": False},
        }


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = "__all__"
