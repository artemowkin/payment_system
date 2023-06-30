from datetime import timedelta, datetime

from fastapi import status, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound, IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt

from .schemas import UserLogin, UserRegistration, DbUser, TokenPair
from .models import User
from ..project.redis import redis_db


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = HTTPBearer()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 60


def _handle_not_found_error(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            return None

    return wrapper


def _handle_unique_violation(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="User with this email already exists")

    return wrapper


class JWTManager:

    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self._secret = secret_key
        self._alg = algorithm

    def _generate_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self._secret, algorithm=self._alg)
        return encoded_jwt

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self._generate_token(data, expires_delta)
        return token

    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta if expires_delta else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        token = self._generate_token(data, expires_delta)
        return token

    def decode_token(self, token: str) -> dict:
        credentials_exception = HTTPException(status.HTTP_403_FORBIDDEN, "Incorrect token")
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._alg])
            if not 'email' in payload or not 'exp' in payload or payload['exp'] <= datetime.utcnow().timestamp():
                raise credentials_exception

            return dict(payload)
        except JWTError:
            raise credentials_exception


class DBAuthentication:

    def __init__(self, session: AsyncSession):
        self._session = session

    @_handle_not_found_error
    async def get_user_by_email(self, email: str) -> DbUser | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return DbUser.from_orm(result.scalar_one())

    @_handle_unique_violation
    async def create_user(self, registration_data: UserRegistration, hashed_password: str) -> DbUser:
        creation_data = registration_data.dict(exclude={'password1', 'password2'})
        stmt = insert(User).returning(User).values(**creation_data, password=hashed_password)
        result = await self._session.execute(stmt)
        return DbUser.from_orm(result.scalar_one())


class SessionsManager:

    def __init__(self):
        self._db = redis_db

    async def add(self, email: str, token_pair: TokenPair) -> None:
        await self._db.hset(email, token_pair.refresh_token, token_pair.access_token)

    async def check_access_token(self, email: str, token: str) -> bool:
        sessions = await self._db.hgetall(email)
        current_sessions = [refresh for refresh in sessions if sessions[refresh] == token.encode()]
        return bool(current_sessions)

    async def check_is_session_active(self, email: str, token: str) -> bool:
        sessions = await self._db.hgetall(email)
        return token.encode() in sessions

    async def clear_refresh_token_sessions(self, email: str, token: str):
        await self._db.hdel(email, token)

    async def delete_by_access_token(self, email: str, token: str):
        sessions = await self._db.hgetall(email)
        refresh_tokens = [refresh for refresh in sessions if sessions[refresh] == token.encode()]
        if not refresh_tokens: return
        await self._db.hdel(email, refresh_tokens[0].decode())


class Authentication:

    def __init__(self, secret_key: str, session: AsyncSession):
        self._db = DBAuthentication(session)
        self._session = SessionsManager()
        self._jwt = JWTManager(secret_key)

    def _generate_token_pair(self, user_email: str) -> TokenPair:
        access_token = self._jwt.create_access_token({'email': user_email})
        refresh_token = self._jwt.create_refresh_token({'email': user_email})
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def login(self, login_data: UserLogin) -> TokenPair:
        db_user = await self._db.get_user_by_email(login_data.email)
        if not db_user or not pwd_context.verify(login_data.password, db_user.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        token_pair = self._generate_token_pair(login_data.email)
        await self._session.add(login_data.email, token_pair)
        return token_pair

    async def registrate(self, registration_data: UserRegistration) -> TokenPair:
        hashed_password = pwd_context.hash(registration_data.password1)
        db_user = await self._db.create_user(registration_data, hashed_password)
        token_pair = self._generate_token_pair(db_user.email)
        await self._session.add(db_user.email, token_pair)
        return token_pair

    async def _get_user_from_token(self, token: str) -> DbUser:
        payload = self._jwt.decode_token(token)
        db_user = await self._db.get_user_by_email(payload['email'])
        if not db_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect token")

        return db_user

    async def get_user_from_access_token(self, token: str) -> DbUser:
        db_user = await self._get_user_from_token(token)
        is_session_active = await self._session.check_access_token(db_user.email, token)
        if not is_session_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect token")

        return db_user

    async def _get_user_from_refresh_token(self, token: str) -> DbUser:
        db_user = await self._get_user_from_token(token)
        is_token_in_session = await self._session.check_is_session_active(db_user.email, token)
        if not is_token_in_session:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Incorrect token")

        return db_user

    async def refresh(self, token: str) -> TokenPair:
        db_user = await self._get_user_from_refresh_token(token)
        await self._session.clear_refresh_token_sessions(db_user.email, token)
        access_token = self._jwt.create_access_token({'email': db_user.email})
        token_pair = TokenPair(access_token=access_token, refresh_token=token)
        await self._session.add(db_user.email, token_pair)
        return token_pair

    async def logout(self, token: str) -> None:
        db_user = await self.get_user_from_access_token(token)
        await self._session.delete_by_access_token(db_user.email, token)
