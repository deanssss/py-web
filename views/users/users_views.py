#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import tornado.web
import logging
from logging.handlers import TimedRotatingFileHandler
from tornado.escape import json_decode
from datetime import datetime

from common.commons import (
    http_response,
)
from common.base import (
    BaseRequestHandler
)
from conf.base import (
    ERROR_CODE,
)
from models import (
    Users,
)

############## Configure logging Start ###############
logFilePath = "log/users/users.log"
logger = logging.getLogger("Users")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(
    logFilePath,
    when="D",
    interval=1,
    backupCount=30
)
formatter = logging.Formatter('%(asctime)s \
    %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)
############## Configure logging End ###############

class RegistHandle(BaseRequestHandler):
    """handle /user/regist request
    :param phone: User sign up phone number
    :param pswd: User sign up password
    :param code: User sign up verify code
    """

    def post(self):
        try:
            # 获取参数
            args = json_decode(self.request.body)
            phone = args['phone']
            pswd = args['pswd']
            code = args['code']
        except:
            # 获取参数失败时
            logger.info("RegistHandle: Request arguements incorrect.")
            http_response(self, ERROR_CODE['1001'], 1001)
            return
        
        ex_user = self.db.query(Users).filter_by(phone=phone).first()
        if ex_user:
            http_response(self, ERROR_CODE['1002'], 1002)
            self.db.close()
            return
        else:
            logger.debug("RegistHandle: insert db, user: %s" %phone)
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_user = Users(phone, pswd, create_time)
            self.db.add(add_user)
            self.db.commit()
            self.db.close()
            # 处理成功
            logger.debug("RegistHandle: Regist successfully.")
            http_response(self, ERROR_CODE['0'], 0)

class LoginHandle(BaseRequestHandler):

    def get(self):
        try:
            phone = self.get_argument("phone")
            pswd = self.get_argument("pswd")
        except:
            logger.info("LoginHandle: request arguement incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return
        
        ex_user = self.db.query(Users).filter_by(phone=phone).first()
        if ex_user:
            logger.debug("LoginHandle: get user login: %s" %phone)
            self.render("index.html")
            self.db.close()
            return
        else:
            http_response(self, ERROR_CODE['1003'], 1003)
            self.db.close()
            return