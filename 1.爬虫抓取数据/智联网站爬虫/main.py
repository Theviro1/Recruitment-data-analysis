import random
import threading
import time

from Executor import Executor


i = 0
executor = Executor()
while executor.scrape_url():
    i += 1
    time.sleep(random.randint(1, 3))  # 暂停1秒缓冲
    if i % 8 == 0:
        time.sleep(60 * 60)  # 爬取8个链接就缓冲60分钟，以免被405拒绝访问
        executor = Executor()


# 多线程爬虫
# def execute():
#     thread_executor = Executor()
#     while thread_executor.scrape_url():
#         pass
#
#
# threads = []
# for i in range(1, 11):
#     thread = threading.Thread(target=execute())
#     threads.append(thread)
#     thread.start()
#
# for thread in threads:
#     thread.join()

