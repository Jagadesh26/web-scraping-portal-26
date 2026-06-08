from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.profiles.models import Profile


class AuthService:

    @staticmethod
    def register_user(validated_data):

        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        Profile.objects.create(
            user=user
        )

        return user

    @staticmethod
    def get_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }