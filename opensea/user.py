import cloudscraper
import json
from loguru import logger
from DBTool import MysqlDB
import re
from retrying import retry

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
proxy = {'https': "http://127.0.0.1:10809"}
base_url = "https://opensea.io/{0}"
next_base_url = 'https://api.opensea.io/api/v1/assets?format=json&order_by=pk&order_direction=desc&limit=50&include_orders=true&asset_contract_address={0}&cursor={1}'
base_user_url = "https://api.opensea.io/api/v1/asset/{0}/{1}/owners?format=json&limit=20&order_by=created_date&order_direction=desc"
db = MysqlDB(
    ip="121.36.38.167", port=3306, db="test", user_name="root", user_pass="bvAdmin123."
)
sql = "SELECT ir_owner FROM `test`.`nft_owners` WHERE `ir_owner` <> '' and owner_state=0 and `ir_owner` not like '0x%' limit 2,100000"
slugs = db.find(sql)


@retry(stop_max_attempt_number=10)
def get_nft_text(slug):
    url = base_url.format(slug)
    print(url)
    resp = scraper.get(url, proxies=proxy)
    if resp.status_code == 200:
        text = resp.text
        # print(text)
        text = re.search('<script id="__NEXT_DATA__" type="application/json"[\s\S]*?>([\s\S]*?)</script>', text).group(
            1)
        if 'relayCache' in text:
            text = json.loads(text)
            address = text["props"]["relayCache"][0][1]["data"]["account"]["address"]
            account = text["props"]["relayCache"][0][1]["data"]["account"]["user"]
            if account:
                account['address'] = address
            else:
                account = dict()
                account['username'] = ''
                account['publicUsername'] = ''
                account['id'] = ''
                account['favoriteAssetCount'] = ''
                account['dateJoined'] = ''
                account['address'] = address
            metadata = text["props"]["relayCache"][0][1]["data"]["account"]["metadata"]
            if metadata:
                if 'isBanned' in str(metadata):
                    metadata.pop('isBanned')
                account['metadata'] = metadata
                instagram = metadata['instagramUsername']
                if instagram:
                    instagram = instagram
                else:
                    instagram = ''
                twitter = metadata['twitterUsername']
                if twitter:
                    twitter = twitter
                else:
                    twitter = ''
                websiteUrl = metadata['websiteUrl']
                if websiteUrl:
                    if 'facebook' in websiteUrl:
                        facebook = websiteUrl
                        websiteUrl = ''
                    else:
                        facebook = ''

                    if 'twitter.' in websiteUrl:
                        twitter = websiteUrl
                        websiteUrl = ''

                    if 'instagram.' in websiteUrl:
                        instagram = websiteUrl
                        websiteUrl = ''
                else:
                    facebook = ''
                    websiteUrl = ''

                if instagram:
                    if 'https:' not in instagram:
                        instagram = 'https://www.instagram.com/' + instagram

                if twitter:
                    if 'https:' not in twitter:
                        twitter = 'https://twitter.com/' + twitter
                account['instagram'] = instagram
                account['twitter'] = twitter
                account['facebook'] = facebook
                account['websiteUrl'] = websiteUrl
                if account['username']:
                    account['url'] = 'https://opensea.io/' + account['username']
                else:
                    account['url'] = 'https://opensea.io/' + account['address']
            logger.info(account)
            db.add_smart('nft_user', account)
            update_sql = "UPDATE `test`.`nft_owners` SET `owner_state` = '1' WHERE `ir_owner_address`='{0}'".format(
                account['address'])
            db.update(update_sql)


if __name__ == '__main__':
    for slug in slugs:
        get_nft_text(slug[0])
