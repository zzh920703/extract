import cloudscraper
import json
import time
from loguru import logger
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import platform
from DBTool import MysqlDB
from retrying import retry

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
proxy = {'https': "http://127.0.0.1:10809"}
base_url = "https://api.opensea.io/api/v1/assets?format=json&include_orders=true&limit=50&order_by=pk&order_direction=desc&asset_contract_address={0}"
next_base_url = 'https://api.opensea.io/api/v1/assets?format=json&include_orders=true&limit=50&order_by=pk&order_direction=desc&asset_contract_address={0}&cursor={1}'
base_user_url = "https://api.opensea.io/api/v1/asset/{0}/{1}/owners?format=json&limit=20&order_by=created_date&order_direction=desc"
db = MysqlDB(
    ip="121.36.38.167", port=3306, db="test", user_name="root", user_pass="bvAdmin123."
)
sql = "select ir_contract_address from nft_contracts where contract_state=0"
slugs = db.find(sql)
logger.info(len(slugs))


@retry(stop_max_attempt_number=10)
def get_nft_text(slug):
    """
    访问接口链接获取NFT信息
    :return:next:翻页标识,text:获取到的响应文本
    """
    url = base_url.format(slug)
    resp = scraper.get(url, proxies=proxy)
    text = resp.text
    text = json.loads(text)
    next = text['next']
    logger.info(next)
    return next, text


@retry(stop_max_attempt_number=10)
def get_nft_next_text(slug, next):
    """
    访问翻页接口链接获取NFT信息
    :param next:
    :return:
    """
    url = next_base_url.format(slug, next)
    resp = scraper.get(url, proxies=proxy)
    text = resp.text
    text = json.loads(text)
    next = text['next']
    logger.info(next)
    return next, text


def parse_nft(text):
    """
    解析响应内容
    :param text:
    :return:
    """
    assets = text['assets']
    if assets:
        for asset in assets:
            item = dict()
            contract_address = asset['asset_contract']['address']
            token_id = asset['token_id']
            item['ir_id'] = contract_address + '_' + token_id
            item['ir_token_id'] = token_id
            item['ir_contract_address'] = contract_address
            item['ir_urlname'] = asset['permalink']
            item['ir_image'] = asset['image_url']
            item['ir_title'] = asset['name']
            try:
                item['ir_owner'] = asset['owner']['user']['username']
            except:
                item['ir_owner'] = ''
            try:
                item['ir_owner_address'] = asset['owner']['address']
            except:
                item['ir_owner_address'] = ''

            creator = asset['creator']
            if creator:
                try:
                    item['ir_creator'] = asset['creator']['user']['username']
                except:
                    item['ir_creator'] = ''
                item['ir_creator_address'] = asset['creator']['address']
            else:
                item['ir_creator'] = ''
                item['ir_creator_address'] = ''
            if not item['ir_creator']:
                item['ir_creator'] = ''

            item['ir_token_standard'] = asset['asset_contract']['schema_name']
            item['ir_blockchain'] = 'Ethereum'

            item['ir_description'] = asset['description']
            if not item['ir_description']:
                item['ir_description'] = ''
            item['ir_platform'] = 'opensea'
            item['ir_lasttime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['ir_collection_name'] = asset['collection']['name']
            item['ir_collection_slug'] = asset['collection']['slug']
            # item['ir_owner_url'] = 'https://opensea.io/' + item['ir_owner_address']
            item['ir_creator_url'] = 'https://opensea.io/' + item['ir_creator_address']
            if item['ir_owner'] == 'NullAddress':
                item['ir_owner'] = item['ir_creator']
                item['ir_owner_address'] = item['ir_creator_address']
                item['ir_owner_url'] = 'https://opensea.io/' + item['ir_creator_address']
            get_user_text(item)


@retry(stop_max_attempt_number=10)
def get_user_text(item):
    """
    请求拥有者链接获取响应内容
    :param item:
    :return:
    """
    user_url = base_user_url.format(item['ir_contract_address'], item['ir_token_id'])
    resp = scraper.get(user_url, proxies=proxy)
    text = resp.text
    parse_user(text, item)


def parse_user(text, item):
    """
    解析拥有者内容
    :param text:
    :param item:
    :return:
    """
    text = json.loads(text)
    owners = text['owners']
    if owners:
        owner_text = owners[0]['owner']
        user = owner_text['user']
        if user:
            username = user['username']
            if username:
                item['ir_owner'] = username
            else:
                item['ir_owner'] = ''
        else:
            item['ir_owner'] = ''
        item['ir_owner_address'] = owner_text['address']
        item['ir_owner_url'] = 'https://opensea.io/' + item['ir_owner_address']
    logger.info(item)
    save(item)
    save_owner(item)
    save_collection(item)
    # save_contract(item)


def save(item):
    """
    保存至ES：索引【nft_opensea】
    :param item:
    :return:
    """
    IS_WINDOWS = platform.system() == "Windows"
    if IS_WINDOWS:
        es = Elasticsearch('http://admin:pUkZaJDU@119.3.168.54:29201/')

    else:
        es = Elasticsearch(['119.3.168.54:29200'])
    logger.info(item)
    actions = []
    action = {}
    action['_index'] = 'nft_opensea'
    action['_type'] = 'bv_dc'
    # unpsert
    action['_op_type'] = 'update'
    action['_retry_on_conflict'] = 1
    action['_id'] = item['ir_id']
    action['_source'] = {
        'doc': {},
        'upsert': item
    }
    actions.append(action)
    bulk(es, actions)


def save_owner(item):
    """
    保存拥有者信息至mysql，用于扩充采集
    :param item:
    :return:
    """
    owner_dict = dict()
    owner_dict['ir_owner'] = item['ir_owner']
    owner_dict['ir_owner_address'] = item['ir_owner_address']
    owner_dict['owner_state'] = '0'
    db.add_smart('nft_owners', owner_dict)


def save_collection(item):
    """
    保存集合信息至mysql，用于扩充采集
    :param item:
    :return:
    """
    collection_dict = dict()
    collection_dict['ir_collection_name'] = item['ir_collection_name']
    collection_dict['ir_collection_slug'] = item['ir_collection_slug']
    collection_dict['collection_state'] = '0'
    db.add_smart('nft_collections', collection_dict)


def run():
    for slug in slugs:
        slug = slug[0]
        next, text = get_nft_text(slug)
        parse_nft(text)
        while next:
            next, text = get_nft_next_text(slug, next)
            parse_nft(text)
        else:
            sql = "UPDATE `nft_contracts` SET `contract_state` = 1 where ir_contract_address='{0}'".format(slug)
            db.update(sql)


if __name__ == '__main__':
    run()
