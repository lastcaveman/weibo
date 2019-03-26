from weibo import User, Post, Search

if __name__ == '__main__':

    search = Search()
    items = search.load('新闻')
    print('search')
    print(items)
    for post in items:
        print(post)
    user = User(6000001234)
    nickname = user._nickname()
    print('user nickname: ')
    print(nickname)
    avatar = user._avatar()
    print('user avatar: ')
    print(avatar)
    statuses_count = user._statuses_count()
    print('user statuses_count: ')
    print(statuses_count)
    description = user._description()
    print('user description: ')
    print(description)
    follow_me = user._follow_me()
    print('user follow_me: ')
    print(follow_me)
    following = user._following()
    print('user following: ')
    print(following)
    followers_count = user._followers_count()
    print('user followers_count: ')
    print(followers_count)
    follow_count = user._follow_count()
    print('user follow_count: ')
    print(follow_count)
    posts = user._posts()
    print('user posts: ')
    print(posts)
    allposts = user._allposts()
    print('user allposts: ')
    print(allposts)

    post = Post(4320019674552079)
    post.load()
    text = post._text()
    print('post text')
    print(text)
    is_long = post._is_long()
    print('post is_long')
    print(is_long)
    is_retweeted = post._is_retweeted()
    print('post is_retweeted')
    print(is_retweeted)
    source_tweeted_id = post._source_tweeted_id()
    print('post source_tweeted_id')
    print(source_tweeted_id)
    source_text = post._source_text()
    print('post source_text')
    print(source_text)
    published_at = post._published_at()
    print('post published_at')
    print(published_at)

    print(post)
