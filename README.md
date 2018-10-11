# PicProbe

## Goal
Utilize various skills to predict the performance of a single photo posted to the "[pics subreddit](https://www.reddit.com/r/pics)" by analyzing images from top posts of all-time on said subreddit.

## Technologies Used
- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [PRAW](https://praw.readthedocs.io/en/latest/) (Python Reddit API Wrapper)
- [AWS Rekognition](https://aws.amazon.com/rekognition/)
- more to come...

## Sample Project Config
(A sample will be uploaded in the future. For now, use the sample below.)
```
import os

PROJECT_NAME = 'PicProbe'

CLIENT_ID = 'XXXXX'
SECRET_ID = 'XXXXX'
USERNAME = 'SampleRedditUsername'

SUBREDDIT = 'pics'

MAX_POSTS = 1000

outfile = 'reddit.json'
target_dir = '{}/data/'.format(os.getcwd())
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

OUTFILE_PATH = target_dir + outfile
```
