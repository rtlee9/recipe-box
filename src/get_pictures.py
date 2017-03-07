from os import path
import argparse

import json
import urllib
import urllib.request

import config
from utils import URL_to_filename

def load_recipes(filename):
    """Load recipes from disk as JSON
    """
    with open(path.join(config.path_data, filename), 'r') as f:
        recipes_raw = json.load(f)
    print('{:,} pictures loaded from disk.'.format(len(recipes_raw)))
    return recipes_raw

def save_picture(recipes_raw, url):
    recipe = recipes_raw[url]
    path_save = path.join(
        config.path_img, '{}.jpg'.format(URL_to_filename(url)))
    if not path.isfile(path_save):
        if 'picture_link' in recipe:
            link = recipe['picture_link']
            if link is not None:
                try:
                    if 'epicurious' in url:
                        img_url = 'https://{}'.format(link[2:])
                        urllib.request.urlretrieve(img_url, path_save)
                    else:
                        urllib.request.urlretrieve(link, path_save)
                except:
                    print('Could not download image from {}'.format(link))

def main(filename, status_interval=500):
    recipes_raw = load_recipes(filename=filename)
    n = len(recipes_raw)
    for i, r in enumerate(recipes_raw.keys()):
        save_picture(recipes_raw, r)
        if i % status_interval == 0:
            print('Downloading image {:,} of {:,}'.format(i, n))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default='recipes_raw.json',
                        help='Recipe JSON file')
    parser.add_argument('--status', type=int, default=50, help='Print status interval')
    args = parser.parse_args()
    main(args.filename, args.status)
