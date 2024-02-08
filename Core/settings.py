
from os import getenv

from dotenv import load_dotenv

load_dotenv()

postgresSQL_password = getenv('database_password')
database_name = getenv('database_name')
sec_key = getenv('SECRET_KEY')
algo = getenv('ALGORITHM')
email_passwrod = getenv('password')
email_sender = getenv('sender')
HOST=getenv('HOST')
PORT=getenv('port')
redis_url=getenv('redis_url')