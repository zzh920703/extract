# -*- coding: utf-8 -*-
import requests
import time
import datetime
from DBTool import MysqlDB
from retrying import retry
from loguru import logger

# 部署在境外服务器上，代码放在opensea目录下


db = MysqlDB(
    ip="114.116.242.191", port=3306, db="diaozheng", user_name="root", user_pass="bvaluate123."
)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
proxy = {'https': "http://127.0.0.1:10809"}
now_timestamp = round(time.time())
base_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=825&range={0}~{1}"
ren_base_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=825&range={0}~{1}&convertId=2787"

@retry(stop_max_attempt_number=10)
def usd_main(start):
    """

    :param start:
    :return:
    """
    start1 = start
    end = start1 + 86399
    url = base_url.format(start1, end)
    logger.info(url)
    response = requests.get(url, headers=headers,proxies=proxy)
    text = response.json()
    points = text['data']['points']
    for timestamp, value in points.items():
        if "'c'" in str(value):
            item = dict()
            item['timestamp'] = timestamp
            item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['timestamp'])))
            item['date'] = time.strftime('%Y-%m-%d', time.localtime(int(item['timestamp'])))
            item['value_usd_usdt'] = value['c'][0]
            item['24hour_value'] = value['c'][1]
            logger.info(item)
            db.add_smart('bijia', item)


@retry(stop_max_attempt_number=10)
def cny_main(start):
    """

    :param start:
    :return:
    """
    start1 = start
    end = start1 + 86399
    url = ren_base_url.format(start1, end)
    response = requests.get(url, headers=headers,proxies=proxy)
    text = response.json()
    points = text['data']['points']
    for timestamp, value in points.items():
        if "'c'" in str(value):
            item = dict()
            item['timestamp'] = timestamp
            # item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['timestamp'])))
            item['value_cny_usdt'] = value['c'][0]
            item['24hour_value_cny'] = value['c'][1]
            logger.info(item)
            db.update_smart('bijia', item, condition='timestamp="{0}"'.format(item['timestamp']))


if __name__ == '__main__':
    # 获取当日日期
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 日期字符串
    # today_date = '2023-02-23'
    # print(type(today_date))
    # 将日期字符串转化为时间元组，struct_time对象，用到time.strptime
    today_time = time.strptime(today_date, "%Y-%m-%d")
    # 将struct_time对象的时间元组转化为时间戳（秒）
    start = int(time.mktime(today_time))
    usd_main(start)
    cny_main(start)
