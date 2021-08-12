import datetime
import sqlalchemy
from sqlalchemy import orm
from db_session import SqlAlchemyBase


class Tyrs(SqlAlchemyBase):
    __tablename__ = 'tyrs'


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Otkuda = sqlalchemy.Column(sqlalchemy.String)
    Kuda = sqlalchemy.Column(sqlalchemy.String)
    Data = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    Dni = sqlalchemy.Column(sqlalchemy.Integer)
    Cena = sqlalchemy.Column(sqlalchemy.Integer)
    Pitanie = sqlalchemy.Column(sqlalchemy.String)
    Level = sqlalchemy.Column(sqlalchemy.String)
    Hotel = sqlalchemy.Column(sqlalchemy.String)