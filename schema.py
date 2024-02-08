from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List


# globally validate the mobile numbers
class UserLogin(BaseModel):
    user_name: str = Field('Enter username')
    password: str = Field('Enter password')


class UserDetails(UserLogin):
    first_name: str = Field('Enter first name', pattern=r'^[A-Z]{1}\D{1,}$')
    last_name: str = Field('Enter last name', pattern=r'^[A-Z]{1}\D{1,}$')
    email: EmailStr  = Field('Enter email',)# Field(pattern=r'^[A-Za-z0-9]\w{8,}')
    # zero or more A-Z,a-z,0-9,any char all digits combination min 8 | not end with spaces
    phone: int =Field('Enter phone number') # = Field(pattern=r'^[6-9]\d{9}$')
    city: str = Field('Enter city')
    state: str = Field('Enter state ')

class UserNotes(BaseModel):
    title: str = Field("Enter title ", pattern=r'^[A-Z]{1}\D{1,}')
    description: str
    color: str
    user_id:int