# -*- coding:utf-8 -*-
import os
import unittest

import time

import re
import urllib,urllib2

import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 定义日志
FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger('tcpserver')

class DownloadImg:
    def __init__(self):
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.PhantomJS()
        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger("AppName")

        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    def download(self, url):
        driver = self.driver

        logger.info("开始下载...")
        # 等待lb 的class出现 超时20s
        driver.get(url)
        logger.info("载中...")

        # page_content = driver.page_source.encode("utf-8")
        # logger.info("=====>" + page_content)

        WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_DivItemDesc img')))
        item_name = driver.find_element_by_css_selector("#content .tb-main-title").text.replace("/", "")
        logger.info(u"获取标题成功" + item_name)
        # item_name = self.find_value(page_content, "itemId") align="absmiddle"

        WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_DivItemDesc img')))
        logger.info(u"获取描述内容成功")
        all_desc_imgs = driver.find_elements_by_css_selector("#J_DivItemDesc img")
        for img in all_desc_imgs:
            img_attr = img.get_attribute("data-ks-lazyload")
            if img_attr is None:
                img_attr = img.get_attribute("src")

            if img_attr is not None and img_attr.endswith(".gif") is False:
                imgUrl = img_attr
                self.save(imgUrl, 'D:/images/' + item_name + "/desc/")

        WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_UlThumb img')))
        logger.info(u"获取轮播图成功")
        all_main_imgs = driver.find_elements_by_css_selector("#J_UlThumb img")
        for img in all_main_imgs:
            imgUrl = img.get_attribute("data-src")
            img = "https:"+imgUrl[:imgUrl.rfind("_")]
            img_400 = img + "_400x400.jpg"
            img_800 = img + "_800x800.jpg"
            self.save(img, 'D:/images/' + item_name + "/main/")
            self.save(img_400, 'D:/images/' + item_name + "/400/")
            self.save(img_800, 'D:/images/' + item_name + "/800/")

        self.driver.close()

    def find_value(self, s, prop):

        regex = prop + '\\s*:\\s+\'(.+)\''
        match = re.search(regex, s)
        if match:
            return match.group(1)
        else:
            logger.info( "not find " + prop + "'s value in string :" + s)
            return None

    def save(self, img_url, dir):
        # 新建目录
        if not os.path.exists(dir):
            os.makedirs(dir)
        try:
            pos = img_url.rfind("/")
            filename = img_url[pos + 1:]
            path = dir + filename
            urllib.urlretrieve(img_url, path)
            logger.info(u"下载:" + img_url + u"成功,保存到:" + path)
        except Exception, e:
            logger.error("Error:" + e.message)
            logger.info(u'【错误】当前图片无法下载:' + img_url)

    def test_log(self):
        logger.debug('this is debug info')
        logger.info('this is information')
        logger.warn('this is warning message')
        logger.error('this is error message')
        logger.fatal('this is fatal message, it is same as logger.critical')
        logger.critical('this is critical message')

if __name__ == "__main__":
    downloadImg = DownloadImg()
    item = raw_input("请输入淘宝的连接：")
    # https://item.taobao.com/item.htm?spm=a219r.lm5644.14.12.70b3a555sLHber&id=44407550968&ns=1&abbucket=12
    # https://item.taobao.com/item.htm?id=44418861346&spm=a21c0.8077897.349447.8.7280428dPzqkcS&type=2&e=m%3D2%26s%3DLVOuwTkFD09w4vFB6t2Z2ueEDrYVVa646og1Ii54c8gYX8TY%2BNEwdw3G0JeI%2FUjeTHm2guh0YLtNDhFsDfpb399zaMqb%2F6lbbEpdulP%2F3FTx65x%2Frj5SHz%2BYs7%2Fl%2BgH1VFZrSPJMs4lBj5mHSeJnGSNsYzxP%2FSkvmfzzQyWfmjYx8Oy1mUIqCA%3D%3D&spm=a21c0.8077897.349447.8.7280428dPzqkcS&type=2&e=m%3D2%26s%3DLVOuwTkFD09w4vFB6t2Z2ueEDrYVVa646og1Ii54c8gYX8TY%2BNEwdw3G0JeI%2FUjeTHm2guh0YLtNDhFsDfpb399zaMqb%2F6lbbEpdulP%2F3FTx65x%2Frj5SHz%2BYs7%2Fl%2BgH1VFZrSPJMs4lBj5mHSeJnGSNsYzxP%2FSkvmfzzQyWfmjYx8Oy1mUIqCA%3D%3D
    downloadImg.download(item)
    downloadImg.test_log()
