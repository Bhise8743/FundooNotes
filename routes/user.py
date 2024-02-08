"""

@Author: Omkar Bhise

@Date: 2024-01-03 11:30:00

@Last Modified by: Omkar Bhise

@Last Modified time: 2024-01-02 02:30:00

@Title :  User Registration

"""
from sqlalchemy.exc import IntegrityError
import warnings
from fastapi import APIRouter, status, Depends, HTTPException
from schema import UserDetails, UserLogin
from fastapi.responses import Response
from sqlalchemy.orm import Session
from model import get_db, User
from Core.utils import hash_password,verify_password,JWT,logger
from task import email_verification
warnings.filterwarnings("ignore")

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED, tags=["User"])
async def user_registration(user: UserDetails, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to takes the information from user and stores on Database

        Parameter: user : UserDetails  => Schema of the user
                        response : Response  it response to the user
                        db: Session = Depends on the get_db  i.e. he yield the database

        Return: JSON form dict in that message, status code, data
    """
    try:
        user_data = user.model_dump()

        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = JWT.encode_data({"user_id": user.id})  # after that token go to the mail id and verify the email
        verify_user_link = f"http://127.0.0.1:8080/user/verify?token={token}"
        email_verification(user.email, verify_user_link)
        return {'message': f"User Added successfully ", 'status': 201, 'data': user_data}
    except IntegrityError as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': "Username or Email is already exist", 'status': 400}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@router.post('/login', status_code=status.HTTP_200_OK, tags=["User"])
def user_login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to takes the information from user and stores on Database

        Parameter: data : UserLogin  => Schema of the userLogin
                    response : Response  it response to the user
                    db: Session = Depends

        Return: JSON form dict in that message, status code

    """
    try:
        # valid_user = db.query(User).filter( log_user.user_name == User.user_name and log_user.password == User.password).first()
        valid_user = db.query(User).filter_by(user_name=data.user_name).one_or_none()
        if not valid_user:
            raise HTTPException(detail='Invalid Username ', status_code=status.HTTP_401_UNAUTHORIZED)
        if not verify_password(data.password, valid_user.password):
            raise HTTPException(detail='Invalid Password ', status_code=status.HTTP_401_UNAUTHORIZED)
        if valid_user.is_verified is False:
            raise HTTPException(detail="Your Username and Password is valid But You are NOT VALID user",
                                status_code=status.HTTP_403_FORBIDDEN)
        return {'message': 'Successfully Logged In', 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}

@router.get('/verify', status_code=status.HTTP_200_OK, tags=["User"])
def verify_token(token: str = None, db: Session = Depends(get_db)):
    try:
        decoded_data = JWT.decode_data(token)
        user_id = decoded_data.get('user_id')  # it get the id form the token only
        user = db.query(User).filter_by(id=user_id).one_or_none()
        if user is None:
            raise HTTPException(detail="User is None", status_code=status.HTTP_401_UNAUTHORIZED)
        user.is_verified = True
        db.commit()
        return {'message': "User Verified successful", 'status': 200, 'data': user}
    except Exception as ex:
        logger.exception(ex)
        return {'message': f"Verification Error {str(ex)}"}


