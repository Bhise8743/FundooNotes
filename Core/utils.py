from fastapi import status, HTTPException, Response, Request, Depends
from datetime import timedelta, datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from model import get_db, User, RequestLog
import pytz
from Core import settings
from passlib.hash import pbkdf2_sha256
import logging
import redis

logging.basicConfig(filename='./fundoo_notes.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


def request_logger(request):
    # Get request details
    session = get_db()
    db = next(session)  # iterator and generator concept  => it give the data line by or one by one
    method = request.method
    path = request.url.path
    log = db.query(RequestLog).filter_by(request_method=method, request_path=path).one_or_none()
    if log is None:
        log = RequestLog(request_method=method, request_path=path, count=1)
        db.add(log)
    else:
        log.count += 1
    db.commit()


def hash_password(password):
    return pbkdf2_sha256.hash(password)


def verify_password(raw_pass, hash_pass):
    return pbkdf2_sha256.verify(raw_pass, hash_pass)


redis_obj = redis.Redis(host=settings.HOST, port=settings.PORT, decode_responses=True)


class Redis:
    @staticmethod
    def add_redis(name, key, value):  # json.dumps(notes_data)  => dict to json formatted string (user,key,json_data)
        return redis_obj.hset(name, key, value)

    @staticmethod
    def get_redis(name, key):  # f user_id and note_id
        return redis_obj.hget(name, key)

    @staticmethod
    def getall_redis(name):  # user_id
        return redis_obj.hgetall(name)

    @staticmethod
    def del_redis(name, key):
        return redis_obj.hdel(name, key)


class JWT:
    @staticmethod
    def encode_data(data: dict):
        if 'exp' not in data:
            expire = datetime.now(pytz.utc) + timedelta(minutes=30)
            data.update({"exp": expire})
        return jwt.encode(data, settings.sec_key, settings.algo)

    @staticmethod
    def decode_data(token):
        try:
            return jwt.decode(token, settings.sec_key, settings.algo)
        except JWTError as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def authentication(request: Request, db: Session = Depends(get_db)):
        token = request.headers.get('authorization')
        decode_token = JWT.decode_data(token)
        user_id = decode_token.get('user_id')
        user = db.query(User).filter_by(id=user_id).one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        request.state.user = user
