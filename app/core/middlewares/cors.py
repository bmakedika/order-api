from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost:3000',
            'http://localhost:8000',
        ],
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allow_headers=['Authorization', 'Content-Type'],
    )