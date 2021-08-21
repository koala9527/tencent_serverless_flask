#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import os

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "deflate",
    "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36",
}

H0 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
H1 = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


class Vibrato():
    """docstring for Vibrato"""

    def __init__(self):
        super(Vibrato, self).__init__()
        self.url = "https://v.douyin.com/nMuYtN/"
        self.headers = HEADERS

    def __get_real_url(self):
        session = requests.Session()
        req = session.get(self.url, timeout=5, headers=self.headers)
        vid = req.url.split("/")[4].split("?")[0]
        videoInfo = session.get("https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + vid,
                                timeout=5, headers=self.headers)
        playAddr = re.findall(
            r'https://aweme.snssdk.com/aweme[\S]*?"', videoInfo.text)[0][:-1]
        parsedAddr = playAddr.replace("/playwm/", "/play/")
        return vid, parsedAddr, session

    def __download(self, vid, info, session):
        print(info)
        self.headers["user-agent"] = H1
        videoBin = session.get(info, timeout=5, headers=self.headers)
        filename = "%s.mp4" % (vid)
        IS_SERVERLESS = bool(os.environ.get('SERVERLESS'))
        UPLOAD_DIR = '/tmp/uploads' if IS_SERVERLESS else os.getcwd() + '/uploads'
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        filePath = os.path.join(UPLOAD_DIR, filename)
        with open(filePath, "wb") as fb:
            fb.write(videoBin.content)
        self.headers["user-agent"] = H0
        return str(vid)

    def run(self, url):
        try:
            self.url = url
            vid, info, session = self.__get_real_url()
            return self.__download(vid, info, session)
        except Exception as e:
            raise e

    def reurl(self, url):
        try:
            self.url = url
            vid, info, session = self.__get_real_url()
            return info
        except Exception as e:
            raise e
