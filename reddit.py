import praw
import json
import time

from config import (
    CLIENT_ID,
    MAX_POSTS,
    OUTFILE_PATH,
    PROJECT_NAME,
    SECRET_ID,
    SUBREDDIT,
    USERNAME,
) 

def authenticate():
    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=SECRET_ID,
                       user_agent=f'{PROJECT_NAME} by {USERNAME}')

def collect_and_write_data(reddit):
    start_time = time.time()

    with open(OUTFILE_PATH, 'w') as f:
        count = 0

        # Non-PRAW endpoint: https://www.reddit.com/r/pics/top/.json?t=all&limit=500
        for submission in reddit.subreddit(SUBREDDIT).top('all', limit=MAX_POSTS):
            # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
            submission = handle_submission_properties(submission)
            json.dump(submission, f, default=lambda o: o.__dict__)
            count += 1

    time_elapsed = round(time.time() - start_time, 3)
    print(f'Wrote {count} lines from {SUBREDDIT} to {OUTFILE_PATH} in {time_elapsed} seconds.')

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

def main():
    """TODO...
    ADD LOGGING FOR:
    1. Process start
    2. Collection/write start
    3. Collection/write end
    4. Process end
    """
    start_time = time.time()
    print(f'Starting {PROJECT_NAME}')
    # Authenticate Reddit w/ credentials
    reddit = authenticate()
    # Retrieve top posts from subreddit + dump to file as JSON
    collect_and_write_data(reddit)

    time_elapsed = round(time.time() - start_time, 3)
    print(f'Finished {PROJECT_NAME} in {time_elapsed} seconds.')

main()
