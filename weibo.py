# -*- coding: utf-8 -*-

import os, json
import requests
import datetime
import configparser

def getConfig(section, key):
    config = configparser.RawConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/.config'
    config.read(path)
    return config.get(section, key)

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
    text = ''
    is_long = False
    is_retweeted = False
    source_tweeted_id = None
    source_text = ''
    published_at = None
    comment = []
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

    def __init__(self, post):
        self.id = post['id']
        try:
            self.id = post['id']
            self.text = post['text']
            self.is_long = post['is_long']
            self.is_retweeted = post['is_retweeted']
            self.source_tweeted_id = post['source_tweeted_id']
        except:
            return 

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'text': self.text,
            'is_long': self.is_long,
            'is_retweeted': self.is_retweeted,
            'source_tweeted_id': self.source_tweeted_id,
            'source_text': self.source_text,
            'published_at': self.published_at,
            'comment': self.comment,
        })

    def load(self):

        url='https://m.weibo.cn/statuses/show'
        params={
            'id':self.id,
            'lang':'zh_CN',
            'ua':'iPhone8,1_iOS12.0.1_Weico_5000_wifi',
        }
        res = requests.get(url, params=params,headers=HEADERS)
        try:
            content = res.json()
        except:
            return 
        self.source_text=content['data']['text']
        GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
        self.published_at=datetime.datetime.strptime(content['data']['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
        

class User:

    id = None
    posts = []
    timeline = []

    def __init__(self, id):
        self.id = id

    def load_timeline(self, num=10):
        url = 'https://m.weibo.cn/feed/friends?max_id='
        headers=HEADERS
        headers['cookie'] = getConfig("user", "cookie")
        res = requests.get(url, headers=headers)
        print(res.content)
        try:
            content = res.json()
        except:
            return []
        print(content)

    def load_posts(self, num=10):
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
            return
        for v in content['data']['cards']:
            if v['card_type'] != 9:
                continue
            post={
                'id' : v['mblog']['id'],
                'text' : v['mblog']['text'],
                'isLongText' : v['mblog']['isLongText'],
                'is_retweeted' : False,
            }
            if 'retweeted_status' in v['mblog'].keys():
                post['is_retweeted'] = True
                post['retweeted_id'] = v['mblog']['retweeted_status']['id']
            post = Post(post) 
            self.posts.append(post)

if __name__ == '__main__':

    # user=User(5687069307)
    # user.load_posts()
    # user.load_timeline()
    # print((user.posts[0].id))
    post={
        'id':'4326563316772008'
    }
    post=Post(post)
    post.load()
    print(post)
    print(post.published_at)
