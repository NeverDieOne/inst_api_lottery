from instabot import Bot
from dotenv import load_dotenv
import os
import re

from pprint import pprint

load_dotenv()


# TODO add any/all
def is_user_exist(username) -> bool:
    if bot.get_user_id_from_username(username):
        return True
    return False


# TODO add new name
def get_users_who_marked_smb(media_id):
    comments = bot.get_media_comments_all(media_id)
    users = []

    for comment in comments:
        if str(comment['user_id']) in users:
            continue

        marked_users = re.findall(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)",
                                  comment['text'])
        if marked_users:
            for user in marked_users:
                if is_user_exist(user):
                    users.append(str(comment['user_id']))

    return users


if __name__ == '__main__':
    bot = Bot()
    bot.login(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))

    link_for_post = 'https://www.instagram.com/p/BtON034lPhu/'
    media_id = bot.get_media_id_from_link(link_for_post)
    media_owner = bot.get_media_owner(media_id)

    users_who_marked_smb = get_users_who_marked_smb(media_id)

    likers = bot.get_media_likers(media_id)
    followers = bot.get_user_followers(media_owner)

    uniq_users = set(users_who_marked_smb).intersection(set(likers)).intersection(set(followers))

    print(len(uniq_users))
    pprint(uniq_users)
