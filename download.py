import json
import requests
import random
from bs4 import BeautifulSoup as BS

from config import (
    IMAGE_DIR,
    OUTFILE_PATH,
) 


class Downloader():

    @staticmethod
    def download_images():
        # Main method to download images from the JSON file in data/
        error_count = 0
        with open(OUTFILE_PATH, 'r') as f:
            data = json.load(f)

            print(f'Downloading {len(data)} images')
            for post in data:
                id_ = post['id']
                url = post['url']

                # Handle flickr URLs (ex. https://www.flickr.com/photos/zaruka/36978499711/)
                if 'flickr.com' in url:
                    url = Downloader.retrieve_flickr_image(url)
                elif 'imgur.com' in url:
                    url = Downloader.retrieve_imgur_image(url)

                result = None
                if url:
                    result = Downloader.download_image_by_url(url, id_)
                
                if not result:
                    error_count += 1

        print(f'{error_count}/{len(data)} errors')

    @staticmethod
    def download_image_by_url(url, image_name):
        r = requests.get(url, stream=True, headers={'User-Agent': Downloader.random_user_agent()})

        if r.status_code == 200:
            filename = f'{IMAGE_DIR}{image_name}.jpg'
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return filename
        else:
            print(url, r.status_code)

        return None

    @staticmethod
    def retrieve_flickr_image(url):
        # Use BeautifulSoup to extract JPG from HTML source code
        r = requests.get(url, stream=True, headers={'User-Agent': Downloader.random_user_agent()})
        if r.status_code == 200:
            soup = BS(r.text, features='html5lib')
            main_photos = soup.find_all('img', class_='main-photo')
            if not main_photos:
                return url

            # ex. "//c1.staticflickr.com/5/4413/36978499711_6a8bf79e3b.jpg"
            src = main_photos[0]['src']
            # Add "_b" directly before ".jpg" to get highest quality image
            id_, _ = src.split('/')[-1].split('.')
            url = src.replace(id_, f'{id_}_b')
            # Just add "https" to URLs without explicit protocol
            if url.startswith('//'):
                url = f'https:{url}'

        return url

    @staticmethod
    def retrieve_imgur_image(url):
        # Convert Imgur page URL to Imgur JPG URL
        # ex. http://imgur.com/LXnMhwi -> http://i.imgur.com/LXnMhwi.jpg
        if 'i.imgur.com' in url:
            return url

        url = url.replace('imgur.com', 'i.imgur.com')
        url = f'{url}.jpg'
        return url

    @staticmethod
    def random_user_agent():
        random_version = random.uniform(50.0, 64.0)
        return f'Mozilla/5.0 (X11; Linux i686; rv:{random_version}) Gecko/20100101 Firefox/{random_version}'
