import traceback

from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from models.crud import *
from models.get_db import get_db
from models.schemas import *
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import *
from common.jsontools import *
from common.logs import logger

usersRouter = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'])


# 校验密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_cure_user(request: Request, token: Optional[str] = Header(...), db: Session = Depends(get_db)) -> UsernameRole:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="验证失败"
    )
    credentials_for_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户未登录或登录token失效"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user_token = await request.app.state.redis.get(username)
        if not user_token and user_token != token:
            raise credentials_for_exception
        user_role = get_role_name(db, get_user_by_username(db, username).role).name
        user = UsernameRole(username=username, role=user_role)
        return user
    except JWTError:
        logger.error(traceback.format_exc())
        raise credentials_exception


# 新建用户
@usersRouter.post("/create", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("创建用户")
    if len(user.username) < 5 or len(user.username) > 16:
        return response(code=100106, message="用户名长度应该是5-16位", data="")
    if user.age < 18:
        return response(code=100103, message="年纪太小不符合", data="")
    if (user.role == "学生" and user.studentnum is None) or (user.role == "教师" and user.jobnum is None) or (
            user.role not in ["教师", "学生"]):
        return response(code=100102, message="身份对应号不匹配", data="")
    db_crest = get_user_by_username(db, user.username)
    if db_crest:
        return response(code=100104, message="用户名重复", data="")
    try:
        user.password = get_password_hash(user.password)
    except Exception as e:
        logger.exception(e)
        return response(code=100105, message="密码加密失败", data="")
    try:
        user = db_create_user(db=db, user=user)
        logger.success("创建用户成功")
        return response(code=0, data={'user': user.username}, message="success")
    except Exception as e:
        logger.exception(e)
        return response(code=100101, message="注册失败", data="")


# 登录
@usersRouter.post("/login", response_model=UserToken, tags=["users"])
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    result = await request.app.state.redis.get(user.username + "_status")
    if not result:
        db_crest = get_user_by_username(db, user.username)
        if not db_crest:
            logger.info("login:" + user.username + "不存在")
            return response(code=100205, message='用户不存在', data="")
        verify_pwd = verify_password(user.password, db_crest.password)
        if verify_pwd:
            user_token = await request.app.state.redis.get(user.username)
            if not user_token:
                try:
                    token = create_access_token(data={"sub": user.username})
                except Exception as e:
                    logger.exception(e)
                    return response(code=100203, message='产生token失败', data="")
                await request.app.state.redis.set(user.username, token, ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
                return response(code=0, message="success", data={"token": token})
            return response(code=100202, message='重复登录', data="")
        else:
            # 密码错误
            result = await request.app.state.redis.hgetall(user.username + "_password")
            if not result:
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                await request.app.state.redis.hset(user.username + "_password", mapping={"num": 0, "time": times})
                return response(code=100206, message="密码错误", data="")
            else:
                error_num = int(result["num"])
                num_time = (datetime.now() - datetime.strptime(result["time"], "%Y-%m-%d %H:%M:%S")).seconds / 60
                if error_num < 10 and num_time < 30:
                    # 更新错误次数
                    error_num += 1
                    await request.app.state.redis.hset(user.username + "_password", 'num', error_num)
                    return response(code=100206, message="密码错误", data="")
                elif error_num < 10 and num_time > 30:
                    # 次数置为1，时间设置为现在时间
                    error_num = 1
                    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                    await request.app.state.redis.hset(user.username + "_password", mapping={"num": error_num, "time": times})
                    return response(code=100206, message="密码错误", data="")
                elif error_num >= 10 and num_time < 30:
                    # 次数设置成最大
                    error_num += 1
                    await request.app.state.redis.hset(user.username + "_password", 'num', error_num)
                    await request.app.state.redis.set(user.username + "_status", "freeze", ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
                    return response(code=100204, message="输入密码错误次数过多，账号暂时锁定，请30分钟后再来登录", data="")
                else:
                    error_num = 1
                    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                    await request.app.state.redis.hset(user.username + "_password", mapping={"num": error_num, "time": times})
                    return response(code=100206, message="密码错误", data="")
    else:
        return response(code=100204, message="输入密码错误次数过多，账号暂时锁定，请30分钟后再来登录", data="")


# 用户信息接口
@usersRouter.get(path="/getUserInfo", response_model=UserBase, tags=["users"])
async def get_cur_user(user: UsernameRole = Depends(get_cure_user), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    data = {'username': db_user.username, 'sex': db_user.sex, 'age': db_user.age}
    if user.role == '学生':
        data['studentnum'] = db_user.studentnum
    else:
        data['jobnum'] = db_user.jobnum
    data['role'] = user.role
    return response(code=0, message="success", data=data)
