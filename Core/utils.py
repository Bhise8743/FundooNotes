from fastapi import status, HTTPException
from datetime import timedelta, datetime
from jose import JWTError, jwt
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
