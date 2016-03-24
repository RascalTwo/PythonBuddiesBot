from . import scraper

#API_STORYINFO = 'https://www.wattpad.com/api/v3/stories/'
#API_HOTSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=hot'
API_NEWSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=new'
#API_STORYTEXT = 'https://www.wattpad.com/apiv2/storytext'
#API_GETCATEGORIES = 'https://www.wattpad.com/apiv2/getcategories'
#API_CHAPTERINFO = 'https://www.wattpad.com/apiv2/info'

async def get_latest_story(session):
    story_json = (await scraper.get_json(session,
                                         API_NEWSTORYLIST,
                                         headers={"User-Agent": "Chrome/41.0.2228.0"}))['stories'][0]
    story_title = story_json['title']
    story_description = story_json['description']
    story_chapter_one_url = story_json['parts'][0]['url']

    return ("**Title:** {}\n"
            "**Description:** {}\n"
            "**Link:** {}"
            .format(story_title,
                    story_description,
                    story_chapter_one_url))
