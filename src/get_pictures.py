from os import path
import json
import urllib
import urllib.request
from bs4 import BeautifulSoup
import config

def load_recipes(filename='recipes_raw.json'):
    """Load recipes from disk as JSON
    """
    with open(path.join(config.path_data, filename), 'r') as f:
        recipes_raw = json.load(f)
    print('{:,} pictures loaded from disk.'.format(len(recipes_raw)))
    return recipes_raw

def save_picture(recipes_raw, url):
    recipe = recipes_raw[url]
    path_save = path.join(config.path_img, '{}.jpg'.format(path.basename(url)))
    if not path.isfile(path_save):
        if 'picture_link' in recipe:
            link = recipe['picture_link']
            if link is not None:
                img_url = 'https://{}'.format(link[2:])
                urllib.request.urlretrieve(img_url, path_save)

def main(status_interval=500):
    recipes_raw = load_recipes()
    n = len(recipes_raw)
    for i, r in enumerate(recipes_raw.keys()):
        save_picture(recipes_raw, r)
        if i % status_interval == 0:
            print('Downloading image {:,} of {:,}'.format(i, n))

if __name__ == '__main__':
    load_recipes()
