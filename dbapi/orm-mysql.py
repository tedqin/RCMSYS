#encoding:utf-8

# SQLAlchemy 是对象映射模型的包，在python中可以定义表
import sqlalchemy
from sqlalchemy import create_engine,MetaData,ForeignKey
from sqlalchemy import Column,Integer,String,and_,Time,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

# 对象映射表
# 分别有学生、书和记录
# 每个类还有属性没有补足
class User(base):
    __tablename__ = 'users'
    uid = Column(String(64),primary_key=True)
    udepartment = Column(String(64),nullable= False)
    urecord = Column(Integer,nullable= False)

    def __repr__(self):
        return self.uid

class Book(base):
    __tablename__ = 'books'
    bid = Column(String(64),primary_key=True)
    bname = Column(String(64),nullable= False)
    bpopularity = Column(Integer,nullable= False)

    def __repr__(self):
        return self.bid

class Record(base):
    __tablename__ = 'records'
    rid = Column(String(64),primary_key=True)
    ruid = Column(String(64),ForeignKey('users.uid'))
    rbid = Column(String(64),ForeignKey('books.bid'))
    rlendtime = Column(Time,nullable= False)
    rreturntime = Column(Time,nullable= False)

    def __repr__(self):
        return self.rid

# 创建数据库连接 参数和连接池大小
engine = create_engine("mysql+pymysql://user:passwd@localhost/yourdb?charset=utf8",max_overflow=20)
DBSession = sessionmaker(bind=engine)

# 创建所有的表
base.metadata.create_all(engine)