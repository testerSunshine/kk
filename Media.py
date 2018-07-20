import copy

from bs4 import BeautifulSoup

from DownloadVideo import downloadVideo
from config.HttpUtils import httpUtils
from config.RedisUtils import redisUtils
from config.urlConf import urls
import re
from config import logger


class media:
    """
    视频连接获取
    """
    def __init__(self):
        self.httpUtils = httpUtils()
        self.redisUtils = redisUtils()
        self.redis_conn = self.redisUtils.redis_conn()
        self.downloadVideo = downloadVideo()

    def get_media_url(self):
        for i in range(1, 84):
            r_urls = copy.deepcopy(urls)
            r_urls["media"]["req_url"] = r_urls["media"]["req_url"].format(i)
            result = self.httpUtils.send(r_urls["media"])
            try:
                if result:
                    self.par_result(result.decode('utf-8'))
            except:
                pass

    def par_result(self, result):
        """
        解析数据
        video_title: 视频标题
        video_time:  视频时长
        video_path: 视频路径
        :param result:
        :return:
        """
        soup = BeautifulSoup(result, 'html.parser')
        li = soup.find_all("li")
        if li:
            for i in range(len(li)-1):
                video_title_re = re.compile("<div class=\"imagesText\">(\S+)</div>")
                video_time_re = re.compile("<p class=\"playTd\">(\S+)</p>")
                video_path_re = re.compile("href=\"(\S+)\">")
                video_title = re.findall(video_title_re, str(li[i]))
                video_time = re.findall(video_time_re, str(li[i]))
                video_path = re.findall(video_path_re, str(li[i]))
                for j in range(len(video_path)):
                    if bytes(video_title[j], encoding="utf8") not in self.redis_conn.lrange("video_title", 0, -1):
                        self.redis_conn.lpush("video_title", video_title[j])
                        self.downloadVideo.get_download_url(video_title=video_title[j],
                                                            video_time=video_time[j],
                                                            video_path=video_path[j],
                                                            )
                    else:
                        logger.log("重复的下载源: {}".format(video_title[j]))
        else:
            logger.log("没有匹配到正确的数据 {}".format(result))


if __name__ == "__main__":
    m = media()
    m.get_media_url()
