import requests
import time
import csv
import codecs
from DBTool import MysqlDB
from DBTool import RedisDB
from retrying import retry

redis_db = RedisDB(ip_ports='localhost:6379', db=0, decode_responses=True)
db = MysqlDB(
    ip="localhost", port=3306, db="test", user_name="root", user_pass="123456"
)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
proxy = {'https': "http://127.0.0.1:10809"}
now_timestamp = round(time.time())
base_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=825&range={0}~{1}&convertId=2787"


@retry(stop_max_attempt_number=10)
def main(start):
    start1 = start
    end = start1 + 86399
    url = base_url.format(start1, end)
    response = requests.get(url, headers=headers, proxies=proxy)
    text = response.json()
    points = text['data']['points']
    datas = list()
    for timestamp, value in points.items():
        item = dict()
        item['timestamp'] = timestamp
        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['timestamp'])))
        item['value_cny_usdt'] = value['c'][0]
        item['24hour_value_cny'] = value['c'][1]
        print(item)
        datas.append(item)
    db.add_batch_smart('bijia1',datas)
    redis_db.sadd('coinmarket_ren', start1)


if __name__ == '__main__':
    # start = 1439222400
    # datetime.datetime.now().strftime("%Y-%m-%d")  # 日期字符串
    while True:
        info = redis_db.sget('coinmarket_ren')
        print(info)
        if info:
            start = int(info[0])
        else:
            start = 1428940800
        if start < now_timestamp:
            main(start)
