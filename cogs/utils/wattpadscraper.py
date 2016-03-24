from . import scraper

#API_STORYINFO = 'https://www.wattpad.com/api/v3/stories/'
#API_HOTSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=hot'
API_NEWSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=new'
#API_STORYTEXT = 'https://www.wattpad.com/apiv2/storytext'
#API_GETCATEGORIES = 'https://www.wattpad.com/apiv2/getcategories'
#API_CHAPTERINFO = 'https://www.wattpad.com/apiv2/info'

async def get_random_story_info(session):
    story_json = (await scraper.get_json(session, API_NEWSTORYLIST, headers={"User-Agent": "Chrome/41.0.2228.0"}))['stories'][0]
    story_title = story_json['title']
    story_description = story_json['description']
    story_id = storyjson['id']
    story_chapteroneurl = story_json['parts'][0]['url']
    story_chapteroneid = storyjson['parts'][0]['id']

    return ('title: ' + story_title +
            'description: ' + story_description +
            'link for furthe reading' + story_chapteroneurl)