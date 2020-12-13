# 3r party
from django.db import models
from django.contrib.postgres.fields import JSONField
import json
import requests


# internal
from user.models import User
from common.consts.base_urls import GOOGLE_AUTH
from django.conf import settings


class SocialApp(models.Model):
    PROVIDERS = (
        ("google", "Google"),
        ("facebook", "Facebook"),
        ("instagram_facebook", "Instagram Facebook"),
    )
    provider = models.CharField(max_length=20,
                                choices=PROVIDERS)
    name = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'provider')

    def __str__(self):
        return f"{self.name} {self.provider}"


class SocialAccount(models.Model):
    provider = models.ForeignKey(SocialApp,
                                on_delete=models.CASCADE,
                                )
    user = models.ForeignKey("user.User",
                             on_delete=models.CASCADE,
                             limit_choices_to={"is_active": True})
    token = models.TextField()
    uid = models.CharField(max_length=255)
    extra_data = JSONField(null=True, blank=True)
    expiry_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')

    def __str__(self):
        return f"{self.user} {self.provider}"

    @classmethod
    def get_social_account(cls, user, provider):
        account = SocialAccount.objects.filter(
            user=user, provider__provider=provider).last()
        return account

    @classmethod
    def social_account_connected(cls, user, provider):
        return SocialAccount.objects.filter(user=user,
            provider__provider=provider).exists()


    def google_get_user_profile(access_token):
        resp = requests.get(GOOGLE_AUTH['profile_url'],
                            params={'access_token': access_token,
                                    'alt': 'json'})
        if resp.status_code == 200:
            resp = resp.json()
            return resp
        else:
            return None

    def get_provider(provider_name):
        return SocialApp.objects.filter(provider=provider_name).first()

    def create_user(user_profile, provider, token):
        user = User.objects.filter(email=user_profile.get('email')).first()
        social_account = SocialAccount(
            provider=provider,
            token = token,
            uid = user_profile.get('id'),
            extra_data = user_profile
            )

        if settings.LINK_SOCIAL_ACCOUNT_WITHOUT_LOGIN and user:
            social_account.user = user
        elif not user:
            user = User(
                email=user_profile.get('email'),
                first_name = user_profile.get('name')
                )
            user.save()
            social_account.user = user
        else:
            return None

        social_account.save()
        return social_account

    def get_social_account(provider, uid):
        return SocialAccount.objects.filter(
            provider=provider,
            uid = uid
            ).first()

    @classmethod
    def google_auth(cls, access_token):
        user_profile = cls.google_get_user_profile(access_token)

        if not user_profile:
            return None

        provider = cls.get_provider('google')

        if not provider:
            return None

        social_account = cls.get_social_account(provider, user_profile.get('id'))

        if not social_account:
            social_account = cls.create_user(user_profile, provider, access_token)

        if social_account:
            return social_account.user
        else:
            return None