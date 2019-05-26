from instabot import Bot
from dotenv import load_dotenv
import os
import re
import random
import argparse


def is_user_exist(username):
    return bool(bot.get_user_id_from_username(username))


def get_users_who_marked_smb(media_id):
    comments = bot.get_media_comments_all(media_id)
    users_who_marked_smb = set()

    for comment in comments:
        # https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
        marked_users = re.findall(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)",
                                  comment['text'])
        if not marked_users:
            continue
        for user in marked_users:
            if is_user_exist(user):
                users_who_marked_smb.add(str(comment['user_id']))
    return list(users_who_marked_smb)


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description='Random winner choise by sub/like/mark smb')
    parser.add_argument('link', help='Link to post')
    args = parser.parse_args()

    bot = Bot()
    bot.login(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))

    link_to_post = args.link
    media_id = bot.get_media_id_from_link(link_to_post)
    media_owner = bot.get_media_owner(media_id)

    markeds = get_users_who_marked_smb(media_id)
    likers = bot.get_media_likers(media_id)
    followers = bot.get_user_followers(media_owner)

    uniq_users = {uniq_user for uniq_user in (markeds + likers + followers)}
    users = [user for user in uniq_users if all([user in markeds, user in likers, user in followers])]

    winner = random.choice(users)
    winner_username = bot.get_user_info(int(winner))['username']
    print(f"Winner is {winner}: {winner_username}")
