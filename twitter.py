import requests


headers = {
    "authority": "api.twitter.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "origin": "https://twitter.com",
    "referer": "https://twitter.com/",
    "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "x-csrf-token": "a3c4b1443de8eb4464bf7b18d4fa461b",
    "x-guest-token": "1630441134076882946",
    "x-twitter-active-user": "yes",
    "x-twitter-client-language": "zh-cn"
}
cookies = {
    "guest_id_marketing": "v1%3A167300265652385164",
    "guest_id_ads": "v1%3A167300265652385164",
    "personalization_id": "\"v1_qhcsLKsHO/OiVD76mlpZqg==\"",
    "guest_id": "v1%3A167300265652385164",
    "_ga": "GA1.2.1251778762.1673516093",
    "ct0": "a3c4b1443de8eb4464bf7b18d4fa461b",
    "at_check": "true",
    "_gid": "GA1.2.117841124.1677551890",
    "des_opt_in": "Y",
    "att": "1-rGpUaELILYEB2dpUa2VRrU2UBQnN1UcsD5kyG01r",
    "_twitter_sess": "BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGbp8pWGAToMY3NyZl9p%250AZCIlMTA4YjhmYWVkZWU0NDc1MmVmYjU5OTk0ZGM2NGVhY2M6B2lkIiUzMWNi%250AMzliNDk3YTRiZDE3N2EyMWNjNjNhOWRmZTVhZQ%253D%253D--12ab48243fb702ce4713b1c83be33f7b38677a65",
    "external_referer": "padhuUp37zgrNDkAw9ihk7kCpgy2Mt9fhqje0OPD9NEwfqqUaalJVMnmvAlQVW36nbs2YDGCarI%3D|0|8e8t2xd8A2w%3D",
    "gt": "1630441134076882946",
    "mbox": "PC#434a9b39b9fd422bb780710e8da51b24.34_0#1740808862|session#09924faf87e0429a954d191b29ebd7a7#1677565922"
}
url = "https://api.twitter.com/2/search/adaptive.json"
params = {
    "include_profile_interstitial_type": "1",
    "include_blocking": "1",
    "include_blocked_by": "1",
    "include_followed_by": "1",
    "include_want_retweets": "1",
    "include_mute_edge": "1",
    "include_can_dm": "1",
    "include_can_media_tag": "1",
    "include_ext_has_nft_avatar": "1",
    "include_ext_is_blue_verified": "1",
    "include_ext_verified_type": "1",
    "skip_status": "1",
    "cards_platform": "Web-12",
    "include_cards": "1",
    "include_ext_alt_text": "true",
    "include_ext_limited_action_results": "false",
    "include_quote_count": "true",
    "include_reply_count": "1",
    "tweet_mode": "extended",
    "include_ext_collab_control": "true",
    "include_ext_views": "true",
    "include_entities": "true",
    "include_user_entities": "true",
    "include_ext_media_color": "true",
    "include_ext_media_availability": "true",
    "include_ext_sensitive_media_warning": "true",
    "include_ext_trusted_friends_metadata": "true",
    "send_error_codes": "true",
    "simple_quoted_tweet": "true",
    "q": "白纸",
    "tweet_search_mode": "live",
    "query_source": "typed_query",
    "count": "20",
    "requestContext": "launch",
    "pc": "1",
    "spelling_corrections": "1",
    "include_ext_edit_control": "true",
    "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe"
}
proxy = {'https': "http://127.0.0.1:10809"}
response = requests.get(url, headers=headers, cookies=cookies, params=params,proxies=proxy)

print(response.text)
print(response)