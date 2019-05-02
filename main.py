from instabot import Bot
from dotenv import load_dotenv
import os
import re

from pprint import pprint

load_dotenv()


def is_user_exist(username) -> bool:
    if bot.get_user_id_from_username(username):
        return True
    return False


def get_marked_users(comment) -> list:
    return re.findall(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)", comment)


if __name__ == '__main__':
    bot = Bot()
    bot.login(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))

    link_for_post = 'https://www.instagram.com/p/BtON034lPhu/'
    media_id = bot.get_media_id_from_link(link_for_post)
    comments = bot.get_media_comments_all(media_id)

    for comment in comments:
        print(f'{comment["user"]["pk"]} - {get_marked_users(comment["text"])}')
