from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader
from Core.utils import JWT, request_logger
from routes.user import user_router
from routes.notes import notes_router
from routes.labels import label_router

app = FastAPI(title="Fundoo Notes")


@app.middleware('/http')
async def add_middleware(request: Request, call_next):
    response = await call_next(request)
    request_logger(request)
    return response

app.include_router(user_router, prefix='/user')
app.include_router(notes_router, prefix='/notes',
                   dependencies=[Security(APIKeyHeader(name='authorization')), Depends(JWT.authentication)])
app.include_router(label_router, prefix='/labels',
                   dependencies=[Security(APIKeyHeader(name='authorization')), Depends(JWT.authentication)])
