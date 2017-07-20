# -*- coding:utf-8 -*-
import os
import unittest

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        # firefoxBin = os.path.abspath(r"C:\soft\chromedriver_win\chromedriver.exe")
        #os.environ["webdriver.chrome.driver"] = firefoxBin
        self.driver = webdriver.Chrome()
        # 隐性等待，最长等30秒
        # self.driver.implicitly_wait(30)

    # def test_search_in_python_org(self):
    #
    #     driver = self.driver
    #     driver.get("http://www.baidu.com")
    #     # self.assertIn("Python", driver.title)
    #     elem = driver.find_element_by_id("kw")
    #     elem.send_keys(u"我是中国人")
    #     elem.send_keys(Keys.ENTER)
    #     #assert "No results found." not in driver.page_source
    #     time.sleep(10)
    #     elem.send_keys(Keys.RETURN)
    #     time.sleep(10)


    def test_login(self):
        driver = self.driver

        # 等待lb 的class出现 超时20s
        driver.get("http://www.baidu.com")
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lb')))

        print "访问成功！！！"

        link = driver.find_element_by_class_name("lb")
        link.click()

        # 等待lb 的class出现 超时20s
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-form')))
        print "跳转登录页成功！！！"

        # 填入账号密码
        username_input = driver.find_element_by_id("TANGRAM__PSP_3__userName")
        username_input.send_keys("zhangyue0808@foxmail.com")

        pwd_input = driver.find_element_by_id("TANGRAM__PSP_3__password")
        pwd_input.send_keys("zhangyue0808")

        inputCode = raw_input("请输入验证码：")
        print "输入的验证码是:" + inputCode
        driver.find_element_by_id("TANGRAM__PSP_3__verifyCode").send_keys(inputCode.decode('utf-8'))

        #登陆
        driver.find_element_by_id("TANGRAM__PSP_3__submit").click()

        # 是否登陆成功
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-name')))
        username = driver.find_element_by_class_name("user-name")
        print "登陆成功:" + username.text.encode("utf-8")

        page_resource = driver.page_source.encode("utf-8")
        print "==========="+page_resource


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()