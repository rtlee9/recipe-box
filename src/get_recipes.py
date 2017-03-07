import json
import time
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import sys
from os import path
import argparse

import config
sys.path.append(config.path_scrapers)
from recipe_scrapers import scrap_me

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

def get_recipe(url):
    try:
        scrap = scrap_me(url)
    except:
        print('Could not scrape URL {}'.format(url))
        return {}

    try:
        title = scrap.title()
    except AttributeError:
        title = None

    try:
        ingredients = scrap.ingredients()
    except AttributeError:
        ingredients = None

    try:
        instructions = scrap.instructions()
    except AttributeError:
        instructions = None

    try:
        picture_link = scrap.picture()
    except AttributeError:
        picture_link = None

    return {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions,
        'picture_link': picture_link,
    }

def get_all_recipes_fn(page_str, page_num):
    base_url = 'http://www.foodnetwork.com'
    search_url_str = 'recipes/a-z'
    url = '{}/{}/{}/p/{}'.format(base_url, search_url_str, page_str, page_num)

    try:
        soup = BeautifulSoup(request.urlopen(
            request.Request(url, headers=HEADERS)).read(), "html.parser")
        recipe_link_items = soup.select('div.o-Capsule__m-Body ul.m-PromoList li a')
        recipe_links = [r.attrs['href']for r in recipe_link_items]
        print('Read {} recipe links from {}'.format(len(recipe_links), url))
        return {r: get_recipe(r) for r in recipe_links}
    except HTTPError:
        print('Could not parse page {}'.format(url))
        return []


def get_all_recipes_ar(page_num):
    base_url = 'http://allrecipes.com'
    search_url_str = 'recipes/?page'
    url = '{}/{}={}'.format(base_url, search_url_str, page_num)

    try:
        soup = BeautifulSoup(request.urlopen(
            request.Request(url, headers=HEADERS)).read(), "html.parser")
        recipe_link_items = soup.select('article > a:nth-of-type(1)')
        recipe_links = list(set(
            [r['href'] for r in recipe_link_items
             if r is not None and r['href'].split('/')[1] == 'recipe']))
        return {base_url + r: get_recipe(base_url + r) for r in recipe_links}
    except HTTPError:
        print('Could not parse page {}'.format(url))
        return []


def get_all_recipes_epi(page_num):
    base_url = 'http://www.epicurious.com'
    search_url_str = 'search/?content=recipe&page'
    url = '{}/{}={}'.format(base_url, search_url_str, page_num)

    try:
        soup = BeautifulSoup(request.urlopen(
            request.Request(url, headers=HEADERS)).read(), "html.parser")
        recipe_link_items = soup.select('div.results-group article.recipe-content-card a.view-complete-item')
        recipe_links = [r['href'] for r in recipe_link_items]
        return {base_url + r: get_recipe(base_url + r) for r in recipe_links}
    except HTTPError:
        print('Could not parse page {}'.format(url))
        return []


def scrape_epi(start_page=1, num_pages=1916, status_interval=50):

    recipes_epi = {}
    start = time.time()
    for i in range(start_page, num_pages + start_page):
        recipes_epi.update(get_all_recipes_epi(i))
        if i % status_interval == 0:
            print('Scraping page {} of {}'.format(i + 1 - start_page, num_pages))
    print('Scraped {} recipes from {} in {:.0f} minutes'.format(
        len(recipes_epi), 'Epicurious.com', (time.time() - start) / 60))

    # Save to disk as JSON
    with open(path.join(config.path_data, 'recipes_raw_epi.json'), 'w') as f:
        json.dump(recipes_epi, f)


def scrape_ar(start_page=1, num_pages=1916, status_interval=50):

    recipes = {}
    start = time.time()
    for i in range(start_page, num_pages + start_page):
        recipes.update(get_all_recipes_ar(i))
        if i % status_interval == 0:
            print('Scraping page {} of {}'.format(i + 1 - start_page, num_pages))
    print('Scraped {} recipes from {} in {:.0f} minutes'.format(
        len(recipes), 'Allrecipes.com', (time.time() - start) / 60))

    # Save to disk as JSON
    with open(path.join(config.path_data, 'recipes_raw_ar.json'), 'w') as f:
        json.dump(recipes, f)


def scrape_fn():
    recipes_fn = {}
    start = time.time()

    # get list of pages with links to recipes
    base_url = 'http://www.foodnetwork.com'
    search_url_str = 'recipes/a-z'
    url = '{}/{}/{}'.format(base_url, search_url_str, '')

    try:
        soup = BeautifulSoup(request.urlopen(
            request.Request(url, headers=HEADERS)).read(), "html.parser")
        page_link_items = soup.select('ul.o-IndexPagination__m-List li a')
        page_links = [p['href'] for p in page_link_items]
    except HTTPError:
        print('Could not parse page {}'.format(url))

    for i, page in enumerate(page_links):
        page_num = 1
        recipe_set = True
        while recipe_set:
            recipe_set = get_all_recipes_fn(path.basename(page), page_num)
            recipes_fn.update(recipe_set)
            page_num += 1
    print('Scraped {} recipes from {} in {:.0f} minutes'.format(
        len(recipes_fn), 'Epicurious.com', (time.time() - start) / 60))

    # Save to disk as JSON
    with open(path.join(config.path_data, 'recipes_raw_fn.json'), 'w') as f:
        json.dump(recipes_fn, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fn', action='store_true', help='Food Network')
    parser.add_argument('--epi', action='store_true', help='Epicurious')
    parser.add_argument('--ar', action='store_true', help='All Recipes')
    parser.add_argument('--status', type=int, default=50, help='Print status interval')
    parser.add_argument('--start', type=int, default=1, help='Start page')
    parser.add_argument('--pages', type=int, default=3000, help='Number of pages to scrape')
    args = parser.parse_args()
    if args.fn:
        scrape_fn()
    if args.epi:
        scrape_epi(args.start, args.pages, args.status)
    if args.ar:
        scrape_ar(args.start, args.pages, args.status)
