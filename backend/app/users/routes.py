from fastapi import APIRouter, Depends

from .schemas import TokenPair, UserLogin, UserRegistration, DbUser, UserOut
from .dependencies import use_authentication, use_token, auth_required
from .services import Authentication


router = APIRouter()


@router.post('/login/', response_model=TokenPair)
async def login(login_data: UserLogin, authentication: Authentication = Depends(use_authentication)):
    tokens = await authentication.login(login_data)
    return tokens


@router.post('/registration/', response_model=TokenPair)
async def registration(registration_data: UserRegistration, authentication: Authentication = Depends(use_authentication)):
    tokens = await authentication.registrate(registration_data)
    return tokens


@router.post('/refresh/', response_model=TokenPair)
async def refresh(refresh_token: str = Depends(use_token), authentication: Authentication = Depends(use_authentication)):
    tokens = await authentication.refresh(refresh_token)
    return tokens


@router.get('/me/', response_model=UserOut)
async def me(user: DbUser = Depends(auth_required)):
    user = UserOut(**user.dict())
    return user


@router.post('/logout/', status_code=204)
async def logout(token: str = Depends(use_token), authentication: Authentication = Depends(use_authentication)):
    await authentication.logout(token)
