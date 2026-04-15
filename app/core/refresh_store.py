import hashlib
from app.core.redis_client import get_redis
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS


TTL_SECONDS = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def store_refresh_token(refresh_token: str, subject: str) -> None:
    redis = get_redis()
    key = f'refresh_token:{_hash(refresh_token)}'
    redis.set(key, subject, ex=TTL_SECONDS)


def get_subject_for_refresh_token(refresh_token: str) -> str:
    redis = get_redis()
    key = f'refresh_token:{_hash(refresh_token)}'
    return redis.get(key)


def revoke_refresh_token(refresh_token: str) -> None:
    redis = get_redis()
    key = f'refresh_token:{_hash(refresh_token)}'
    redis.delete(key)