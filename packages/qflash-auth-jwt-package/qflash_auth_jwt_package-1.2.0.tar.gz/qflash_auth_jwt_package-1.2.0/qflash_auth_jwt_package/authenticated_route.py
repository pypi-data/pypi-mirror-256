from fastapi import Depends
from fastapi.routing import APIRoute

from qflash_auth_jwt_package.jwt import JWT


jwt = JWT()


class AuthenticatedRoute(APIRoute):
    def __init__(self,*args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(jwt.auth_wrapper))
        kwargs["dependencies"] = dependencies
        super(AuthenticatedRoute, self).__init__(*args, **kwargs)


class AuthenticateUserApiClientdRoute(APIRoute):
    def __init__(self,*args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(jwt.auth_user_api_client))
        kwargs["dependencies"] = dependencies
        super(AuthenticateUserApiClientdRoute, self).__init__(*args, **kwargs)


class AuthenticateAdminRoute(APIRoute):
    def __init__(self,*args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(jwt.auth_admin))
        kwargs["dependencies"] = dependencies
        super(AuthenticateAdminRoute, self).__init__(*args, **kwargs)


class AuthenticateAllRoute(APIRoute):
    def __init__(self,*args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(jwt.auth_all))
        kwargs["dependencies"] = dependencies
        super(AuthenticateAllRoute, self).__init__(*args, **kwargs)
