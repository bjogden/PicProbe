import praw
import time

from config import (
    CLIENT_ID,
    MAX_POSTS,
    PROJECT_NAME,
    SECRET_ID,
    SUBREDDIT,
    USERNAME,
)


class Reddit():
    def __init__(self):
        self.reddit = self.authenticate()

    def authenticate(self):
        return praw.Reddit(client_id=CLIENT_ID,
                           client_secret=SECRET_ID,
                           user_agent=f'{PROJECT_NAME} by {USERNAME}')

    @staticmethod
    def handle_submission_properties(obj):
        # We cannot serialize these object to JSON, so we need to remove them, unfortunately.
        if obj._reddit:
            del obj._reddit
        if obj.subreddit:
            del obj.subreddit
        if obj.author:
            # May as well save author name (in case we need it in the future).
            obj.author_name = obj.author.name
            del obj.author
        if obj._flair:
            del obj._flair
        if obj._mod:
            del obj._mod
        if obj._comments_by_id:
            del obj._comments_by_id

        return obj

    def collect_data(self):
        start_time = time.time()
        count = 0
        posts = []
        # Non-PRAW endpoint: https://www.reddit.com/r/pics/top/.json?t=all&limit=500
        for submission in self.reddit.subreddit(SUBREDDIT).top('all', limit=MAX_POSTS):
            # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
            submission = Reddit.handle_submission_properties(submission)
            posts.append(submission)
            count += 1

        time_elapsed = round(time.time() - start_time, 3)
        print(f'Collected {count} posts from {SUBREDDIT} in {time_elapsed} seconds.')
        return posts
