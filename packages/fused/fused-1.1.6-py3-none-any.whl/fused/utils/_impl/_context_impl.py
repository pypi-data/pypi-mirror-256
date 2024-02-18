from fused._auth import CREDENTIALS
from fused.api.api import FusedAPI


def context_get_user_email() -> str:
    api = FusedAPI()
    return api._whoami()["email"]


# TODO: Used??
def context_get_auth_token() -> str:
    return CREDENTIALS.credentials.access_token
