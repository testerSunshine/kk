# -*- coding: utf8 -*-
import pymysql
from pymysql import DataError, InternalError

from config import logger
from config.now_time import get_now_time
from config.yaml_info import _get_yaml_local


class MysqlConn:
    pymysql.install_as_MySQLdb()

    def __init__(self):
        self.conn = self.mysql_conn()
        self.cur = self.conn.cursor()

    def mysql_conn(self):
        y = _get_yaml_local("config_video.yaml")
        conn = pymysql.connect(
                host=y["db"]["ip"],
                port=y["db"]["port"],
                user=y["db"]["uname"],
                passwd=y["db"]["passwd"],
                db=y["db"]["table"],
                charset="utf8mb4"
                )
        conn.autocommit(1)
        return conn

    def execute_m(self, sql):
        if sql is None:  # sql not None!
            return "please input sql"
        else:
            try:
                self.cur.execute(sql)
                logger.log(u"数据执行完毕..")
                return self.cur.fetchall()
            except DataError as e:
                logger.log(e)
            except InternalError as e:
                logger.log(e)
            except pymysql.err.Error as e:
                logger.log(e)
                self.conn = self.mysql_conn()  # mysql 断开连接重连
                self.execute_m(sql)

    def close_session(self):
        self.cur.close()
        self.conn.close()

    def l_time(self):
        return self.conn.escape(get_now_time("%Y-%m-%d %H:%M:%S"))

    def insert_video(self, video_title, video_time, video_path):
        """
        插入视频信息
        :return:
        """
        video_title = self.conn.escape(video_title)
        video_time = self.conn.escape(video_time)
        video_path = self.conn.escape(video_path)
        video_author = self.conn.escape("看看")
        video_author_id = self.conn.escape(1)
        video_channel = self.conn.escape(1)
        sql = "insert into video_library (" \
              "video_length, " \
              "video_title," \
              "video_path, " \
              "video_author, " \
              "video_author_id," \
              " video_channel, " \
              "video_create_time, " \
              "video_update_time) values " \
              "({0},{1},{2},{3},{4},{5},{6},{7})".format(video_time,
                                                         video_title,
                                                         video_path,
                                                         video_author,
                                                         video_author_id,
                                                         video_channel,
                                                         self.l_time(),
                                                         self.l_time(),
                                                         )
        self.execute_m(sql)


if __name__ == "__main__":
    pass
