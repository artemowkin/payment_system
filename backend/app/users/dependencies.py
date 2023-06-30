from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .services import Authentication, oauth2_scheme
from .schemas import DbUser
from ..project.settings import settings
from ..project.dependencies import use_session


def use_authentication(session: AsyncSession = Depends(use_session)) -> Authentication:
    return Authentication(settings.secret_key, session)


def use_token(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    return credentials.credentials


async def auth_required(token: str = Depends(use_token), authentication: Authentication = Depends(use_authentication)) -> DbUser:
    user = await authentication.get_user_from_access_token(token)
    return user
