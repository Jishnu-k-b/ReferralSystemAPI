from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("user_details/", views.user_details),
    path("referrals_list/", views.referral_view),
]
