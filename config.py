# 配置文件

EVENT = 'test'

# mysql
HOST = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'root'
TEST_DB = 'test'
PRODUCT_DB = 'subject_demo'
DB_TEST_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{TEST_DB}?charset=utf8'
DB_PRODUCT_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{PRODUCT_DB}?charset=utf8'


if EVENT == 'test':
    DB_URI = DB_TEST_URI
else:
    DB_URI = DB_PRODUCT_URI


# redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = 0

REDIS_URI = f'redis://:@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# jwt
SECRET_KEY = '17fc974383002573c1922d529b558dee0ccbe062569d04ef1ad953abae688c25'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

