# -*- coding: utf-8 -*-

import os
import json
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


class Search:

    line = []

    def load(self, keyword, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {
            'containerid': '100103type=61&q='+keyword,
            'page': page,
            'page_type': 'searchall',
        }
        headers = HEADERS
        res = requests.get(url, params=params, headers=headers)
        try:
            content = res.json()
        except:
            return []
        items = []
        for v in content['data']['cards'][0]['card_group']:
            post = Post(v['mblog'])
            self.line.append(post)
            items.append(post)
        return items


class Post:

    id = None

    def __init__(self, post):
        if isinstance(post, int):
            self.id = post
        elif isinstance(post, dict):
            self.pics = []
            if 'pics' in post.keys():
                for v in post['pics']:
                    if 'large' in v.keys():
                        self.pics.append(v['large']['url'])
                    else:
                        self.pics.append(v['url'])                
            if 'id' in post.keys():
                self.id = post['id']
            if 'text' in post.keys():
                self.text = post['text']
            if 'isLongText' in post.keys():
                self.is_long = post['isLongText']
            if 'isLongText' in post.keys() and 'text' in post.keys():
                if not self.is_long:
                    self.source_text = self.text
            if 'retweeted_status' in post.keys():
                self.is_retweeted = True
                self.source_tweeted_id = post['retweeted_status']['id']
            else:
                self.is_retweeted = False
                self.source_tweeted_id = None
            if 'edit_at' in post.keys():
                GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
                self.published_at = datetime.datetime.strptime(
                    post['edit_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
            elif 'created_at' in post.keys() and len(post['created_at']) > 10:
                GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
                self.published_at = datetime.datetime.strptime(
                    post['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
            else:
                self.published_at = ''
            if 'user' in post.keys():
                self.user = User(post['user'])

    def __str__(self):
        if hasattr(self, 'source_text'):
            source_text = self.source_text
        else:
            source_text = ''
        return json.dumps({
            'id': self.id,
            'text': self.text,
            'is_long': self.is_long,
            'is_retweeted': self.is_retweeted,
            'source_tweeted_id': self.source_tweeted_id,
            'source_text': source_text,
            'pics': self.pics,
            'published_at': self.published_at,
        }, ensure_ascii=False)

    def _text(self):
        if not hasattr(self, 'text'):
            self.load()
        return self.text

    def _is_long(self):
        if not hasattr(self, 'is_long'):
            self.load()
        return self.is_long

    def _is_retweeted(self):
        if not hasattr(self, 'is_retweeted'):
            self.load()
        return self.is_retweeted

    def _source_tweeted_id(self):
        if not hasattr(self, 'source_tweeted_id'):
            self.load()
        return self.source_tweeted_id

    def _source_text(self):
        if not hasattr(self, 'source_text'):
            self.load()
        return self.source_text

    def _published_at(self):
        if not hasattr(self, 'published_at'):
            self.load()
        return self.published_at

    def _comment(self):
        if not hasattr(self, 'comment'):
            self.comment = []
            self.load()
        return self.comment

    def _user(self):
        if not hasattr(self, 'user'):
            self.load()
        return self.user

    def load(self):
        url = 'https://m.weibo.cn/statuses/show'
        params = {
            'id': self.id,
            'lang': 'zh_CN',
            'ua': 'iPhone8,1_iOS12.0.1_Weico_5000_wifi',
        }
        res = requests.get(url, params=params, headers=HEADERS)
        try:
            content = res.json()
        except:
            return
        post = content['data']
        self.text = post['text']
        self.is_long = post['isLongText']
        self.source_text = post['text']

        self.pics = []
        if 'pics' in post.keys():
            for v in post['pics']:
                if 'large' in v.keys():
                    self.pics.append(v['large']['url'])
                else:
                    self.pics.append(v['url'])
        if 'retweeted_status' in post.keys():
            self.is_retweeted = True
            self.source_tweeted_id = post['retweeted_status']['id']
        else:
            self.is_retweeted = False
            self.source_tweeted_id = None
        GMT_FORMAT = '%a %b %d %H:%M:%S %z %Y'
        self.published_at = datetime.datetime.strptime(
            post['created_at'], GMT_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
        self.user = User(post['user'])


class User:

    id = None
    cookie = None

    def __init__(self, user):
        if isinstance(user, int):
            self.id = user
        elif isinstance(user, dict):
            self.id = user['id']
            self.nickname = user['screen_name']
            self.avatar = user['avatar_hd']
            self.statuses_count = user['statuses_count']
            self.follow_me = user['follow_me']
            self.description = user['description']
            self.following = user['following']
            self.followers_count = user['followers_count']
            self.follow_count = user['follow_count']

    def set_cookie(self, cookie):
        self.cookie = cookie

    def _nickname(self):
        if not hasattr(self, 'nickname'):
            self.load()
        return self.nickname

    def _avatar(self):
        if not hasattr(self, 'avatar'):
            self.load()
        return self.avatar

    def _statuses_count(self):
        if not hasattr(self, 'statuses_count'):
            self.load()
        return self.statuses_count

    def _description(self):
        if not hasattr(self, 'description'):
            self.load()
        return self.description

    def _follow_me(self):
        if not hasattr(self, 'follow_me'):
            self.load()
        return self.follow_me

    def _following(self):
        if not hasattr(self, 'following'):
            self.load()
        return self.following

    def _followers_count(self):
        if not hasattr(self, 'followers_count'):
            self.load()
        return self.followers_count

    def _follow_count(self):
        if not hasattr(self, 'follow_count'):
            self.load()
        return self.follow_count

    def _posts(self):
        if not hasattr(self, 'posts'):
            self.load_posts()
        return self.posts

    def _timeline(self):
        if not hasattr(self, 'timeline'):
            self.timeline = []
            self.load_timeline()
        return self.timeline

    def _allposts(self):
        if not hasattr(self, 'all_posts'):
            self.load_allposts()
        return self.posts

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
        }, ensure_ascii=False)

    def load(self):
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {
            'type': 'uid',
            'value': self.id,
            'containerid': '100505'+str(self.id),
        }
        res = requests.get(url, params=params, headers=HEADERS)
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
        headers = HEADERS
        headers['cookie'] = self.cookie
        res = requests.get(url, headers=headers)
        try:
            content = res.json()
        except:
            return []
        for v in content['data']['statuses']:
            post = Post(v)
            self.timeline.append(post)

    def load_allposts(self):
        if not hasattr(self, 'posts'):
            self.posts = []
        statuses_count = self._statuses_count()
        page = ceil(statuses_count / 10) + 1
        while page > 0:
            self.load_posts(page)
            page = page-1

    def load_posts(self, page=1, since_id=''):
        if not hasattr(self, 'posts'):
            self.posts = []
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {
            'type': 'uid',
            'value': self.id,
            'containerid': '107603' + str(self.id),
            'page': page,
            'since_id': since_id,
        }
        res = requests.get(url, params=params, headers=HEADERS)
        try:
            content = res.json()
        except:
            return
        for v in content['data']['cards']:
            if v['card_type'] != 9:
                continue
            post = Post(v['mblog'])
            self.posts.append(post)
