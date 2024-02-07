from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader

from routes.user import router

app = FastAPI(title="Fundoo Notes")

app.include_router(router, prefix='/user')
