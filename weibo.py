# -*- coding: utf-8 -*-

import os, json
import requests
import datetime
import configparser
from math import ceil

def getConfig(section, key):
    config = configparser.RawConfigParser()
    path = '.config'
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
    user = None

    def __init__(self, post):
        if 'id' in post.keys():   
            self.id = post['id']
        if 'text' in post.keys():   
            self.text = post['text']
        if 'isLongText' in post.keys():   
            self.is_long = post['isLongText']
        if 'retweeted_status' in post.keys():   
            self.is_retweeted = True
            self.source_tweeted_id = post['retweeted_status']['id']
        if 'edit_at' in post.keys():
            GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
            self.published_at=datetime.datetime.strptime(post['edit_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
        elif 'created_at' in post.keys() and len(post['created_at'])>10:
            GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
            self.published_at=datetime.datetime.strptime(post['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
        if 'user' in post.keys():   
            self.user = User(post['user'])

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
            # 'user': json.dumps(self.user),
        })

    def text(self):
        return self.text

    def is_long(self):
        return self.is_long

    def is_retweeted(self):
        return self.is_retweeted

    def source_tweeted_id(self):
        return self.source_tweeted_id

    def source_text(self):
        return self.source_text

    def published_at(self):
        return self.published_at

    def comment(self):
        return self.comment

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
        self.user = User(content['data']['user'])
        self.source_text=content['data']['text']
        GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
        self.published_at=datetime.datetime.strptime(content['data']['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')

class User:

    id = None
    posts = []
    timeline = []

    def __init__(self, user):
        if isinstance(user,int):
            self.id = user
        elif isinstance(user,dict):
            self.id = user['id']
            self.nickname = user['screen_name']
            self.avatar = user['avatar_hd']
            self.statuses_count = user['statuses_count']
            self.follow_me = user['follow_me']
            self.description = user['description']
            self.following = user['following']
            self.followers_count = user['followers_count']
            self.follow_count = user['follow_count']

    def nickname(self):
        return self.nickname
    
    def avatar(self):
        return self.avatar

    def statuses_count(self):
        return self.statuses_count

    def follow_me(self):
        return self.follow_me

    def description(self):
        return self.description

    def following(self):
        return self.following

    def followers_count(self):
        return self.followers_count

    def follow_count(self):
        return self.follow_count
        
    def __str__(self):
        return json.dumps({
            'id': self.id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'statuses_count': self.statuses_count,
            'follow_me': self.follow_me,
            'description': self.description,
            'following': self.following,
            'followers_count': self.followers_count,
            'follow_count': self.follow_count,
        })

    def load(self):
        url = '?type=uid&value=1750349192&containerid=1005051750349192'
        url='https://m.weibo.cn/api/container/getIndex'
        params={
            'type':'uid',
            'value':self.id,
            'containerid':'100505'+str(self.id),
        }
        res = requests.get(url, params=params,headers=HEADERS)
        try:
            content = res.json()
        except:
            return 
        self.id = content['data']['userInfo']['id']
        self.nickname = content['data']['userInfo']['screen_name']
        self.avatar = content['data']['userInfo']['avatar_hd']
        self.statuses_count = content['data']['userInfo']['statuses_count']
        self.follow_me = content['data']['userInfo']['follow_me']
        self.description = content['data']['userInfo']['description']
        self.following = content['data']['userInfo']['following']
        self.followers_count = content['data']['userInfo']['followers_count']
        self.follow_count = content['data']['userInfo']['follow_count']

    def load_alltimeline(self):
        print('1')

    def load_timeline(self, num=10):
        url = 'https://m.weibo.cn/feed/friends?max_id='
        headers=HEADERS
        headers['cookie'] = getConfig("weibo-user", "cookie")
        res = requests.get(url, headers=headers)
        try:
            content = res.json()
        except:
            return []
        for v in content['data']['statuses']:
            post = Post(v) 
            self.timeline.append(post)

    def load_allposts(self):
        
        page = ceil(self.statuses_count / 10) + 1
        while page>0:
            self.load_posts(page)
            page=page-1

    def load_posts(self, page=1,since_id=''):
        url = 'https://m.weibo.cn/api/container/getIndex'
        params={
            'type': 'uid',
            'value': self.id,
            'containerid': '107603' + str(self.id),
            'page': page,
            'since_id': since_id,
        }
        res = requests.get(url, params=params,headers=HEADERS)
        try:
            content = res.json()
        except:
            return
        for v in content['data']['cards']:
            if v['card_type'] != 9:
                continue
            post = Post(v['mblog']) 
            self.posts.append(post)


