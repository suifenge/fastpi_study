from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from datetime import datetime
from models.database import Base, engine


class User(Base):
    """用户基础表"""
    __tablename__ = 'users'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=32), unique=True, index=True)  # 用户名
    password = Column(String(length=252))  # 密码
    status = Column(Integer, default=0)  # 状态 1 删除 0 正常
    jobnum = Column(Integer, nullable=True)  # 工号
    studentnum = Column(Integer, nullable=True)  # 学号
    age = Column(Integer)  # 年龄
    sex = Column(String(length=8), default='男')  # 性别
    role = Column(Integer, ForeignKey('roles.id'))  # 角色
    addtime = Column(DateTime, default=datetime.now())  # 注册时间






class Role(Base):
    """角色表"""
    __tablename__ = 'roles'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=8), unique=True, index=True)  # 角色名


class Course(Base):
    """课程表"""
    __tablename__ = 'courses'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=252), unique=True, index=True)  # 课程名称
    icon = Column(String(length=252), nullable=True)  # icon
    desc = Column(String(252), nullable=True)  # 描述
    status = Column(Boolean, default=False)  # 状态
    onsale = Column(Boolean, default=False)  # 是否上架
    catalog = Column(Text, nullable=True)  # 目录
    owner = Column(Integer, ForeignKey('users.id'))  # 拥有者
    likenum = Column(Integer, default=0)  # 点赞数


class StudentCourse(Base):
    """学生课程表"""
    __tablename__ = 'studentcourses'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    students = Column(Integer, ForeignKey('users.id'))  # 学生
    course = Column(Integer, ForeignKey('courses.id'))  # 课程
    addtime = Column(DateTime, default=datetime.now())  # 加入时间
    updatetime = Column(DateTime, default=addtime)  # 更新时间
    status = Column(Integer, default=0)  # 状态 1 删除 0 正常


class CommentCourse(Base):
    """课程评论"""
    __tablename__ = 'commentcourses'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    course = Column(Integer, ForeignKey('courses.id'))  # 课程id
    user = Column(Integer, ForeignKey('users.id'))  # 评论人
    pid = Column(Integer, ForeignKey('commentcourses.id'))  # 回复
    addtime = Column(DateTime, default=datetime.now())  # 添加时间
    top = Column(Boolean, default=False)  # 是否置顶
    context = Column(Text)
    status = Column(Integer, default=0)  # 状态 1 删除 0 正常


class Message(Base):
    """消息表"""
    __tablename__ = 'messages'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True, index=True)
    senduser = Column(Integer, ForeignKey('users.id'))  # 发送者
    acceptuser = Column(Integer, ForeignKey('users.id'))  # 接收者
    read = Column(Boolean, default=False)  # 是否已读，接收者是否已读
    sendtime = Column(String(length=252))  # 发送时间
    pid = Column(Integer, ForeignKey('messages.id'))
    addtime = Column(DateTime, default=datetime.now())  # 添加时间
    context = Column(Text)
    status = Column(Integer, default=0)  # 状态 1 删除 0 正常


Base.metadata.create_all(bind=engine)
