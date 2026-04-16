from app.core.redis_client import get_redis

def blacklist_jti(jti: str, ttl_seconds: int) -> None:
    redis = get_redis()
    key = f'jwt_blacklist:{jti}'
    redis.set(key, '1', ex=ttl_seconds)

def is_jti_blacklisted(jti: str) -> bool:
    redis = get_redis()
    key = f'jwt_blacklist:{jti}'
    return redis.exists(key) == 1