"""Obfuscate recipe sources by hashing."""
import json
import logging
from os import path
from bcrypt import gensalt, hashpw
from tqdm import tqdm
import argparse

# logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def get_salt(salt_filename='.salt.txt'):
    """Read salt from disk and create new one if doensn't exist."""
    try:  # try reading salt from disk
        with open(salt_filename, 'rb') as f:
            salt = f.read()
        logger.debug('Salt {} read from {}'.format(salt, salt_filename))
    except FileNotFoundError:  # if not found then create and persist
        logger.info('No salt found on disk; generating new one')
        salt = gensalt(6)
        with open(salt_filename, 'wb') as f:
            f.write(salt)
        logger.debug('Salt {} saved to {}'.format(salt, salt_filename))
    return salt


def get_data(filename):
    """Load recipe data from disk."""
    with open(filename, 'r') as f:
        recipes = json.load(f)
    logger.info('Read {:,} recipes from {}'.format(len(recipes), filename))
    return recipes


def hash_url(url, salt):
    """Hash a URL using bcrypt `hashpw` and bcrype `salt`."""
    return hashpw(url.encode('utf-8'), salt).split(salt)[1].decode("utf-8")


def main(source):
    """Obfuscate recipe sources by hashing."""
    salt = get_salt()
    filename = path.join('data', 'recipes_raw_{}.json'.format(source))
    recipes = get_data(filename)

    recipes_nosource = {}
    for url, recipe in tqdm(recipes.items()):
        url_hash = hash_url(url, salt)
        if 'picture_link' in recipe and recipe['picture_link'] is not None:
            recipe['picture_link'] = hash_url(recipe['picture_link'], salt)
        recipes_nosource[str(url_hash)] = recipe

    filename_out = path.join('data', 'recipes_raw_nosource_{}.json'.format(source))
    with open(filename_out, 'w') as f:
        json.dump(recipes_nosource, f, indent=2)
    logger.info('Wrote {:,} recipes to {}'.format(len(recipes_nosource), filename_out))

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--fn', action='store_true', help='Food Network')
    parser.add_argument('--epi', action='store_true', help='Epicurious')
    parser.add_argument('--ar', action='store_true', help='All Recipes')
    args = parser.parse_args()

    if args.fn:
        main('fn')
    if args.epi:
        main('epi')
    if args.ar:
        main('ar')
