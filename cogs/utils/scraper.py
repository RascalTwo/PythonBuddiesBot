import asyncio
import json
from discord.ext import commands

categories = ['hot', 'new', 'controversial', 'rising', 'top']


async def get_subreddit_json(session, subreddit, category):
    return await get_json(session, 'https://www.reddit.com/r/' + subreddit + '/' + category + '/.json')

async def get_json(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def get_post_from_json(post_data : dict):
    post = post_data['data']
    score = post['score']
    author = post['author']
    isNSFW = post['over_18']
    link = post['url']
    title = post['title']
    return '**Title:** {0}\n**Link:** <{1}>\n**Author:** {2}\n**Score:** {3}\n**NSFW:** {4}'.format(title, link, author, score, isNSFW)

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
    sr_data = await get_subreddit_json(session, subreddit, category)
    sr_posts = sr_data['data']['children']
    return await get_posts(sr_posts, num)
