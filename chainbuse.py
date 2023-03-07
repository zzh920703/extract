# -*- coding: utf-8 -*-
import requests
import json
import dateparser
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import platform

#部署在192上，放在私募数据采集文件夹

headers = {
    "authority": "www.chainabuse.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
cursor = 'YXJyYXljb25uZWN0aW9uOjA='
chains = ['ETH', 'BTC', 'POLYGON', 'SOL', 'TRON']
url = "https://www.chainabuse.com/api/graphql-proxy"


def save(item):
    """
    存储
    :param item:
    :return:
    """
    IS_WINDOWS = platform.system() == "Windows"
    if IS_WINDOWS:
        es = Elasticsearch('http://admin:pUkZaJDU@119.3.168.54:29201/')
    else:
        es = Elasticsearch(['192.168.1.252:29200', '192.168.1.74:29200'])
    index_type = item.pop('index_type')

    actions = []
    action = {}
    action['_index'] = index_type
    action['_type'] = 'bv_dc'
    # unpsert
    action['_op_type'] = 'update'
    action['_retry_on_conflict'] = 1
    action['_id'] = item['IR_SID']
    action['_source'] = {
        'doc': {},
        'upsert': item
    }
    actions.append(action)
    bulk(es, actions)


def run(cursor, chain):
    """
    爬取各链风险信息
    :param cursor:
    :param chain:
    :return:
    """
    data = {
        "operationName": "GetReports",
        "variables": {
            "input": {
                "chains": [
                    chain
                ],
                "scamCategories": [],
                "orderBy": {
                    "field": "CREATED_AT",
                    "direction": "DESC"
                }
            },
            "first": 15,
            "after": cursor
        },
        "query": "query GetReports($input: ReportsInput, $after: String, $before: String, $last: Float, $first: Float) {\n  reports(\n    input: $input\n    after: $after\n    before: $before\n    last: $last\n    first: $first\n  ) {\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n      __typename\n    }\n    edges {\n      cursor\n      node {\n        ...Report\n        __typename\n      }\n      __typename\n    }\n    count\n    totalCount\n    __typename\n  }\n}\n\nfragment Report on Report {\n  id\n  ...ReportPreviewDetails\n  ...ReportAccusedScammers\n  ...ReportAuthor\n  ...ReportAddresses\n  ...ReportCompromiseIndicators\n  __typename\n}\n\nfragment ReportPreviewDetails on Report {\n  createdAt\n  scamCategory\n  categoryDescription\n  biDirectionalVoteCount\n  viewerDidVote\n  description\n  lexicalSerializedDescription\n  commentsCount\n  source\n  checked\n  __typename\n}\n\nfragment ReportAccusedScammers on Report {\n  accusedScammers {\n    id\n    info {\n      id\n      contact\n      type\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReportAuthor on Report {\n  reportedBy {\n    id\n    username\n    trusted\n    __typename\n  }\n  __typename\n}\n\nfragment ReportAddresses on Report {\n  addresses {\n    id\n    address\n    chain\n    domain\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment ReportCompromiseIndicators on Report {\n  compromiseIndicators {\n    id\n    type\n    value\n    __typename\n  }\n  __typename\n}\n"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)

    text = response.json()
    # cursor = text['data']['reports']['pageInfo']['endCursor']

    edges = text['data']['reports']['edges']
    for edge in edges:
        # print(edge)
        item = dict()
        item['createtime'] = edge['node']['createdAt']
        item['createtime'] = dateparser.parse(item['createtime']).strftime('%Y-%m-%d %H:%M:%S')
        item['IR_TYPE'] = edge['node']['scamCategory']
        item['IR_CONTENT'] = edge['node']['description']
        # item['createtime'] = edge['createdAt']
        addresses = edge['node']['addresses']
        addrs = list()
        for address in addresses:
            addr = address['address']
            if addr:
                addrs.append(addr)
        item['IR_ADDRESS'] = ';'.join(addrs)
        item['IR_LASTTIME'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['IR_LOADTIME'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['IR_SID'] = edge['node']['id']
        item['IR_URLNAME'] = 'https://www.chainabuse.com/report/' + item[
            'IR_SID'] + '?context=browse-chain&chain=' + chain
        item['IR_SITENAME'] = 'chainabuse'
        item['IR_NETWORK'] = chain
        item['index_type'] = 'clue_analysis'
        item['IR_PRIORITY'] = -1
        print(item)
        # save(item)


if __name__ == '__main__':
    for chain in chains:
        run(cursor, chain)
