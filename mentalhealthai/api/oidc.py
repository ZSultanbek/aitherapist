from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class KeycloakOIDCBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super().create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def get_userinfo(self, access_token, id_token, payload):
        data = super().get_userinfo(access_token, id_token, payload)
        return data
