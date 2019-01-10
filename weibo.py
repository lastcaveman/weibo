# -*- coding: utf-8 -*-

import os, json
import requests
import datetime

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
class Post:

    id = None
    text = None
    is_long = False
    is_retweeted = False
    source_tweeted_id = None

    # headers = {
    #     'Cookie': '',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    #     'cache-control': 'max-age=0',
    #     'dnt': '1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    # }

    def __init__(self, type, post):
        self.id = post['id']
        if type=='postlist':
            self.id = post['id']
            self.text = post['text']
            self.is_long = post['is_long']
            self.is_retweeted = post['is_retweeted']
            self.source_tweeted_id = post['source_tweeted_id']
        
        if type=='load':
            url='https://m.weibo.cn/statuses/show'
            params={
                'id':self.id,
                'aid':'01An4-ozO4lq-nST9dg2jG1mPpYoJvVw_kdqRkacF_05bF8Hc.',
                'c':'weicoios',
                'count':'100',
                'from':'1233293010',
                'gsid':'_2A2526lAgDeRxGeBJ7loQ8yjIzzWIHXVTvuTorDV6PUJbi9AKLRf-kWpNRlWs0RKHSGmScW9Unwf9o2D5ROsYrO0A',
                'i':'7303aad',
                'lang':'zh_CN',
                'max_id':'3892098619272065',
                's':'78c0b746',
                'ua':'iPhone8,1_iOS12.0.1_Weico_5000_wifi',
                'uid':'5687069307',
                'v_f':'1',
                'v_p':'59',
            }
            res = requests.get(url, params=params,headers=HEADERS)
            try:
                content = res.json()
            except:
                print('1')
            self.source_text=content['data']['text']
            GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'

            self.published_at=datetime.datetime.strptime(content['data']['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
            

class User:

    id = None


    def __init__(self, id):
        self.id = id

    def get_timeline(self, num=10):
        url = 'https://m.weibo.cn/feed/friends?max_id='
        res = requests.get(url, headers=self.headers)
        print(res.content)
        try:
            content = res.json()
        except:
            return []
        print(content)

    def get_posts(self, num=10):
        url = 'https://m.weibo.cn/api/container/getIndex'
        params={
            'type': 'uid',
            'value': self.id,
            'containerid': '107603' + str(self.id),
            'page': '1',
            'since_id': '',
        }
        res = requests.get(url, params=params,headers=HEADERS)
        try:
            content = res.json()
        except:
            return []
        posts = []
        for v in content['data']['cards']:
            print(v)
            if v['card_type'] != 9:
                continue
            post={
                'id' : v['mblog']['id'],
                'text' : v['mblog']['text'],
                'isLongText' : v['mblog']['isLongText'],
                'isRetweeted' : False,
            }
            if 'retweeted_status' in v['mblog'].keys():
                post['isRetweeted'] = True
                post['retweeted_id'] = v['mblog']['retweeted_status']['id']
            posts.append(post)
        return posts

if __name__ == '__main__':

    user=User(5687069307)
    posts = user.get_posts()
    print(json.dumps(posts))
    post={
        'id':'4326563316772008'
    }
    post=Post('load',post)
    print(post)
