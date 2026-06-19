from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class ProjectJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        messages = []

        for token_class in (AccessToken, RefreshToken):
            try:
                return token_class(raw_token)
            except Exception as exc:
                messages.append(
                    {
                        "token_class": token_class.__name__,
                        "token_type": token_class.token_type,
                        "message": str(exc),
                    }
                )

        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )
