import copy
import os
import re
import time
import requests

from config.HttpUtils import httpUtils
from config.db_tools import MysqlConn
from config.urlConf import urls
from config import logger


class downloadVideo:
    """
    下载视频
    """
    def __init__(self):
        self.httpUtils = httpUtils()
        self.db_tools = MysqlConn()

    def get_download_url(self, video_title, video_time, video_path):
        """
        获取视频下载源
        :return:
        """
        d_urls = copy.deepcopy(urls)
        if video_path:
            d_urls["get_download_url"]["req_url"] = d_urls["get_download_url"]["req_url"].format(
                video_path
            )
            result = self.httpUtils.send(urls=d_urls["get_download_url"])
            if result:
                data_video_re = re.compile("data-video=\"//(\S+)\"")
                data_video_url = re.search(data_video_re, result.decode("utf-8")).group(1)
                self.get_video(data_video_url=data_video_url, video_title=video_title, video_time=video_time,)
        else:
            logger.log("当前视频下载队列空，程序暂停1h...")
            time.sleep(3600)

    def get_video(self, video_title, video_time, data_video_url):
        """
        解析视频链接，下载
        :return:
        """
        if data_video_url:
            header = {'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)'}
            try:
                response = requests.get("http://{0}".format(data_video_url),
                                        headers=header,
                                        stream=True)
                mp4 = data_video_url.split("/")[-1]
                file_path = "{0}/{1}/{2}".format(os.getcwd(), "video", mp4)
                if not os.path.exists(file_path):
                    with open(file_path, 'wb')as f:
                        f.write(response.content)
                        f.close()
                        print("视频下载成功")
                        self.db_tools.insert_video(video_title, video_time, "/video/"+mp4)
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass


if __name__ == "__main__":
    d = downloadVideo()
    d.get_download_url()