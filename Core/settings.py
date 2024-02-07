
from os import getenv

from dotenv import load_dotenv

load_dotenv()

postgresSQL_password = getenv('database_password')
database_name = getenv('database_name')