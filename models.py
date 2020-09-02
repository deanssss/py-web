#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import sys
from conf.base import BaseDB, engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

class Users(BaseDB):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True)
    createTime = Column(DateTime, nullable=True)

    def __init__(self, phone, pswd, createTime):
        self.phone = phone
        self.password = pswd
        self.createTime = createTime

def initdb():
    BaseDB.metadata.create_all(engine)

if __name__ == "__main__":
    print ("Initlialize database")
    initdb()