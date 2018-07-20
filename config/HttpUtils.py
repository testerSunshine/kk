# -*- coding: utf8 -*-
import json
import socket
import random
from time import sleep
import requests
from requests_toolbelt import MultipartEncoder

from config import logger


class httpUtils(object):

    def __init__(self):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.initS()
        self._cdn = None

    # def get_proxy(self):
    #     """
    #     获取代理
    #     :return:
    #     """
    #     p = proxy()
    #     return p.get_filter_proxy()
    #
    # def random_proxy(self):
    #     """
    #     随机代理
    #     :return:
    #     """
    #     proxy_list = self.get_proxy()
    #     http_proxy = {"http": "http://{}".format(proxy_list[random.randint(0, len(proxy_list) - 1)])}
    #     logger.log(u"当前代理ip: {0}".format(http_proxy))
    #     return http_proxy

    def initS(self):
        self._s = requests.Session()
        self._s.headers.update(self._set_header())
        return self

    def set_cookies(self, **kwargs):
        """
        设置cookies
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self._s.cookies.set(k, v)

    def del_cookies(self):
        """
        删除所有的key
        :return:
        """
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        """
        删除指定key的session
        :return:
        """
        self._s.cookies.set(key, None)

    def _set_header(self):
        """设置header"""
        return {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D100 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN",
        }

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def resetHeaders(self):
        self._s.headers.clear()
        self._s.headers.update(self._set_header())

    def getHeadersHost(self):
        return self._s.headers["Host"]

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def getHeadersReferer(self):
        return self._s.headers["Referer"]

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self

    @property
    def cdn(self):
        return self._cdn

    @cdn.setter
    def cdn(self, cdn):
        self._cdn = cdn

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        # r_proxy = self.random_proxy()  # 获取随机代理ip
        allow_redirects = False
        is_logger = urls["is_logger"]
        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        self.setHeadersReferer(urls["Referer"])
        if data:
            method = "post"
            # self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        if "is_multipart_data" in urls and urls["is_multipart_data"]:
            data = MultipartEncoder(data)
            self.setHeaders({"Content-Type": data.content_type})
            self.setHeaders(urls.get("headers", {}))
        else:
            self.setHeaders(urls.get("headers", {}))
            # self.setHeaders({"Content-Type": "application/json"})
        if is_logger:
            logger.log(
                u"url: {0}\n入参: {1}\n请求方式: {2}\n".format(urls["req_url"], data, method,))
        if self.cdn:
            url_host = self.cdn
        else:
            url_host = urls["Host"]
        for i in range(urls["re_try"]):
            try:
                # sleep(urls["s_time"]) if "s_time" in urls else sleep(0.001)
                sleep(urls.get("s_time", 0.001))
                requests.packages.urllib3.disable_warnings()
                response = self._s.request(method=method,
                                           timeout=2,
                                           url="https://" + url_host + urls["req_url"],
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           # proxies=r_proxy,
                                           **kwargs)
                if response.status_code == 200 or response.status_code == 201:
                    if response.content:
                        if is_logger:
                            logger.log(
                                u"出参：{0}".format(response.content))
                        return json.loads(response.content) if urls["is_json"] else response.content
                    else:
                        logger.log(
                            u"url: {} 返回参数为空".format(urls["req_url"]))
                        return error_data
                elif response.status_code == 403:
                    logger.log("ip 被封，{}".format(response.content))
                    sleep(60*60*2)  # ip被封，自动休眠一小时
                else:
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
            except KeyError:
                pass
        return error_data
