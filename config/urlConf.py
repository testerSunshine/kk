# -*- coding: utf8 -*-

urls = {
    "media": {  # 获取视频源
        "req_url": "/media/page_{}/",
        "req_type": "get",
        "Referer": "https://www.qiushibaike.com/media",
        "Host": "www.qiushibaike.com",
        "re_try": 1,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": False,
        "is_multipart_data": False,
        "headers": {
        }
    },
    "get_download_url": {  # 获取视频源
        "req_url": "{}",
        "req_type": "get",
        "Referer": "https://www.qiushibaike.com/media",
        "Host": "www.qiushibaike.com",
        "re_try": 1,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": False,
        "is_multipart_data": False,
        "headers": {
        }
    }

}