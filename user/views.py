from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import random
import string

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, ReferralSerializer
from .models import User, Referral
from rest_framework.pagination import PageNumberPagination


def generate_referral_code():
    characters = string.ascii_letters + string.digits
    referral_code = "".join(random.choices(characters, k=10))
    while User.objects.filter(my_referral_code=referral_code).exists():
        referral_code = "".join(random.choices(characters, k=10))
    return referral_code

# register view

@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["my_referral_code"] = generate_referral_code()
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        referral_code = request.data.get("referral_code")
        user.save()
        # when the referral code is inputted saves the referral info
        if referral_code:
            try:
                referring_user = User.objects.get(
                    my_referral_code=referral_code,
                )
                Referral.objects.create(
                    referring_user=referring_user,
                    referred_user=user,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid referral code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"id": user.id, "message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login view 
# login to get the access token for the authorization

@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    user_data = {
        "id": serializer.data.get("id"),
        "first_name": serializer.data.get("first_name"),
        "last_name": serializer.data.get("last_name"),
        "my_referral_code": serializer.data.get("my_referral_code"),
    }
    return Response(
        {
            "token": token.key,
            "user": user_data,
        }
    )

# user details view
# views the user details of the current logged in user using authorization token
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    user_details = {
        "username": user.username,
        "email": user.email,
        "referral_code": user.referral_code,
        "my_referral_code": user.my_referral_code,
        "created_at": user.created_at,
    }
    return Response(user_details)

# referral list view
# shows the referral details of the current logged in user using authorization token
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def referral_view(request):
    user = request.user
    referrals = Referral.objects.filter(referring_user=user).order_by(
        "-created_at"
    )  # refferals
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_referrals = paginator.paginate_queryset(referrals, request)
    serializer = ReferralSerializer(paginated_referrals, many=True)
    return paginator.get_paginated_response(serializer.data)
