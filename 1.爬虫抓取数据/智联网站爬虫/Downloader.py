import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class Downloader:
    # 自定义ip代理池，避免IP被封禁
    proxy_pool = [
        "49.7.213.148:50004",
    ]
    driver = None
    proxy = ""

    def __init__(self):
        pass
        # 随机选取一个ip
        self.proxy = random.choice(self.proxy_pool)
        # selenium驱动访问接口
        options = webdriver.ChromeOptions()
        # 添加代理ip
        # options.add_argument("--proxy-server=http://" + self.proxy)
        # 反爬关闭webdriver标识
        options.add_argument("--disable-blink-features=AutomationControlled")
        # 关闭webRTC
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        options.add_experimental_option("prefs", preferences)
        self.driver = webdriver.Chrome(options=options)  # 初始化打开一个足够以免总是重复打开

    def download(self, url):
        self.driver.get(url)
        # 处理反爬滑块验证
        actions = ActionChains(self.driver)
        try:
            element_slider = self.driver.find_element(By.ID, "nc_1_n1z")  # 找到验证滑块
            # 循环随机慢速滑动防止被机器识别
            actions.click_and_hold(element_slider).perform()
            for i in range(1, 5):
                off = random.randint(40, 80)
                actions.move_by_offset(off, 0).pause(0.1).perform()
            actions.drag_and_drop_by_offset(element_slider, 100, 0).perform()
        except:
            pass
        # 完成访问
        return self.driver.page_source
