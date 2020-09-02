#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:deansql@localhost:3306/demo?charset=utf8', encoding="utf8", echo=False)
BaseDB = declarative_base()

SERVER_HEADER = "http://localhost:8000"

ERROR_CODE = {
    "0": "ok",
    "1001": "wrong parameters",
    "1002": "the phone has been registed",
    "1003": "the user not exists",

    "2001": "Upload image can not be empty",
}