import time

from reddit import Reddit
from download import Downloader
from utils import write_data
from config import (
    LOCAL,
    PROJECT_NAME,
)


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

    # No need to hit API to collect data if we can just use the sample data
    if not LOCAL:
        # Authenticate Reddit w/ credentials
        reddit = Reddit()
        # Retrieve top posts from subreddit
        post_data = reddit.collect_data()
        # Dump post data to file as JSON
        write_data(post_data)
    else:
        print('LOCAL: True; skipping PRAW to use sample-reddit.json')

    # Download images using data recently saved in JSON file
    Downloader.download_images()

    time_elapsed = round(time.time() - start_time, 3)
    print(f'Finished {PROJECT_NAME} in {time_elapsed} seconds.')


if __name__ == '__main__':
    main()
