from pydantic import BaseModel as basemodel


class LoginRequest(basemodel):
    username: str
    password: str

class TokenResponse(basemodel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

class RefreshRequest(basemodel):
    refresh_token: str

class LogoutRequest(basemodel):
    refresh_token: str