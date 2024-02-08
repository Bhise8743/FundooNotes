from fastapi import status, HTTPException,Response,Request,Depends
from datetime import timedelta, datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from model import get_db,User
import pytz
from Core import settings
from passlib.hash import pbkdf2_sha256
import logging
logging.basicConfig(filename='./fundoo_notes.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

def hash_password(password):
    return pbkdf2_sha256.hash(password)


def verify_password(raw_pass, hash_pass):
    return pbkdf2_sha256.verify(raw_pass, hash_pass)


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
    def jwt_authentication(request: Request, db: Session = Depends(get_db)):
        token = request.headers.get('authorization')
        decode_token = JWT.decode_data(token)
        user_id = decode_token.get('user_id')
        user = db.query(User).filter_by(id=user_id).one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        request.state.user = user