from weibo import User,Post

if __name__ == '__main__':

    # user={
    #     'id':'1750349192'
    # }
    user=User(1664708001)
    user.load()
    # user.load_allposts()
    user.load_posts(10)
    for post in user.posts:
        print(post.id)
    user=User(4326563316772008)
    user.load_posts()
    user.load_timeline()
    print((user.timeline))
    post={
        'id':'4326563316772008'
    }
    post=Post(post)
    post.load()
    print(post.user)
    print(post.published_at)