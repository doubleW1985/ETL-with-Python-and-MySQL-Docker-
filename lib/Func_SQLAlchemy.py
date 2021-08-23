# -*- coding: utf-8 -*-
from sqlalchemy import create_engine


class SQLAlchemy():
    def __init__(self, Database_Type, User, Pwd, Host, Port, Database):
        self.DB_Type = Database_Type
        self.DB_User = User
        self.DB_Pwd = Pwd
        self.DB_Host = Host
        self.DB_Port = Port
        self.DB_Database = Database

    def create_engine(self):
        connect_string = '{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            self.DB_Type, self.DB_User, self.DB_Pwd, self.DB_Host, self.DB_Port, self.DB_Database)
        engine = create_engine(connect_string)

        return engine
