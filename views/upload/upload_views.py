#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import tornado.web
import os
import logging
import json
from logging.handlers import TimedRotatingFileHandler
from tornado.escape import json_decode

from common.commons import (
    http_response,
    save_files,
)
from common.base import (
    BaseRequestHandler
)
from conf.base import (
    ERROR_CODE,
    SERVER_HEADER,
)

########## Configure logging #############
logFilePath = "log/upload/upload.log"
logger = logging.getLogger("Upload")  
logger.setLevel(logging.DEBUG)  
handler = TimedRotatingFileHandler(logFilePath,  
                                   when="D",  
                                   interval=1,  
                                   backupCount=30)  
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)  
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)

class UploadFileHandle(BaseRequestHandler):
    def post(self):
        try:
            image_metas = self.request.files['image']
        except:
            logger.info("UploadFileHandle: request arguement incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return
        
        image_url = ""
        image_path_list = []
        if image_metas:
            pwd = os.getcwd()
            save_image_path = os.path.join(pwd, "static/image/")
            logger.debug("UploadFileHandle: save image path: %s" %save_image_path)
            file_name_list = save_files(image_metas, save_image_path)
            image_path_list = [SERVER_HEADER + "/static/image/" + i for i in file_name_list]
            ret_data = {"imageUrl": image_path_list}
            self.write(json.dumps(
                {
                    "data": {
                        "msg": ret_data,
                        "code": 0
                    }
                }
            ))
        else:
            logger.info("UploadFileHandle: image stream is empty")
            http_response(self, ERROR_CODE['2001'], 2001)