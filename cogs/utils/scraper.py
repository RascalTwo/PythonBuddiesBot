categories = ['hot', 'new', 'controversial', 'rising', 'top']

async def get_subreddit_json(session, subreddit, category):
    return await get_json(session, 'https://www.reddit.com/r/' + subreddit + '/' + category + '/.json')

async def get_json(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def get_post_from_json(post_data: dict):
    from datetime import datetime
    post = post_data['data']
    score = post['score']
    author = post['author']
    is_nsfw = post['over_18']
    link = post['url']
    title = post['title']

    timediff = datetime.now() - datetime.fromtimestamp(post['created_utc'])
    days = timediff.days
    hours = timediff.seconds // 3600
    minutes = (timediff.seconds // 60)% 60
    created = []

    if days != 0:
        if days > 1:
            created.append(str(days) + ' days')
        else:
            created.append(str(days) + ' day')
    if hours != 0:
        if hours > 1:
            created.append(str(hours) + ' hours')
        else:
            created.append(str(hours) + ' hour')
    if minutes != 0:
        if minutes > 1:
            created.append(str(minutes) + ' minutes')
        else:
            created.append(str(minutes) + ' minute')

    return  '''**Title:** {0}
**Link:** <{1}>
**Author:** {2}
**Created:** {3} ago
**Score:** {4}
**NSFW:** {5}'''.format(title, link, author, ' '.join(created), score, is_nsfw)

async def get_posts(sr_posts, num):
    posts = []
    i = 0
    for post in sr_posts:
        if i >= num:
            break
        posts.append(await get_post_from_json(post))
        i += 1
    return posts

async def get_subreddit_top(session, subreddit, num, category):
    try:
        sr_data = await get_subreddit_json(session, subreddit, category)
        sr_posts = sr_data['data']['children']
    except KeyError:
        return ['Posts could not be loaded, are you sure thats a subreddit?']
    return await get_posts(sr_posts, num)
