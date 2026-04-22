from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.redis_client import get_redis


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        protected_prefixes = ('/orders', '/invoices', '/users/me')

        if not path.startswith(protected_prefixes):
            return await call_next(request)

        redis = get_redis()
        client_ip = request.client.host

        if path.startswith('/orders'):
            bucket, limit, ttl_seconds = 'orders', 120, 300
        elif path.startswith('/invoices'):
            bucket, limit, ttl_seconds = 'invoices', 60, 300
        else:
            bucket, limit, ttl_seconds = 'users_me', 30, 300

        key = f'rate_limit:{bucket}:{client_ip}'
        current_count = redis.incr(key)
        if current_count == 1:
            redis.expire(key, ttl_seconds)
        if current_count > limit:
            return JSONResponse(
                status_code=429,
                content={'detail': 'Too many requests. Please try again later.'},
            )

        return await call_next(request)


def register_rate_limit(app: FastAPI) -> None:
    app.add_middleware(RateLimitMiddleware)