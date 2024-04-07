from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    my_referral_code = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Referral(models.Model):
    referring_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referred_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
