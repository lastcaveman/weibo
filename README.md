# weibo

### 介绍 ###
----

weibo 采用 Python 编写，用来方便地获取微博上各种内容的信息.

**注: 本项目代码均在 macOS 10.14.2 上使用 python3.7 编写和测试通过，其他环境可能存在一定问题。**

### 快速开始 ###
---------

准备

**克隆本项目**
```
  git clone git@github.com:lastcaveman/weibo.git
  cd weibo
```

**解决依赖**

* `requests <https://github.com/kennethreitz/requests>`
* `datetime <https://github.com/zopefoundation/DateTime>`
* `configparser <https://docs.python.org/3/library/configparser.html>`


```
  sudo pip install -r requirements.txt
```

or

```
  sudo pip2 install -r requirements.txt
```

### User:用户 ###
---------
User 代表一个用户, 处理知乎问题相关操作. 创建一个 User 对象需传入该用户的 ID ，如：

```
    from weibo import User
    user = User(1750349192)
```

通过 ID 得到 User 对象后, 可以加载用户信息:
```
    user = user.load()
```
然后获取该用户的一些信息:

```
    # -*- coding: utf-8 -*-
    from weibo import User
    
    user = User(1750349192)
    user = user.load()

    # 获取该用户的昵称
    nickname = user.get_nickname()
    
    # 获取该用户的头像
    avatar = user.get_avatar()
    
    # 获取该用户的动态条数
    statuses_count = user.get_statuses_count()
    
    # 获取该用户的签名
    description = user.get_description()
    
    # 获取该用户是否关注当前登录用户
    follow_me = user.get_follow_me()
    
    # 获取当前登录用户是否关注该用户
    following = user.get_following()
    
    # 获取关注该用户的用户数
    followers_count = user.get_followers_count()
    
    # 获取该用户关注的用户数
    follow_count = user.get_follow_count()
    
    # 获取该用户的首页动态
    posts = user.get_posts()
    
    # 获取该用户的全部动态
    posts = user.get_allposts()
```