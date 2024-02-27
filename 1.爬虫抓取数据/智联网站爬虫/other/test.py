import random

from selenium import webdriver
import requests


proxy_pool = [
        "49.7.213.148:50004",
    ]

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 无头浏览器，不在打开页面
# 获取代理ip
proxy = random.choice(proxy_pool)
options.add_argument("--proxy-server=https://" + proxy)
# 清除Webdriver启动痕迹
options.add_argument("--disable-blink-features=AutomationControlled")
# 关闭WebRTC
preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(options)
# 获取当前ip地理位置和时区
ip = "98.98.45.198"
response = (requests.get(f"http://ip-api.com/json/{ip}")).json()
geolocation = {
    "latitude": response["lat"],
    "longitude": response["lon"],
    "accuracy": 1
}
timezone = {
    "timezoneId": response["timezone"]
}
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", geolocation)
driver.execute_cdp_cmd("Emulation.setTimezoneOverride", timezone)
driver.get("https://browserleaks.com/ip")
input()
driver.close()
