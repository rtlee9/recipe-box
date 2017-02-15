import json
import time
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import sys
import config
sys.path.append(config.path_scrapers)
from recipe_scrapers import scrap_me

base_url = 'http://www.epicurious.com'

def get_recipe(url):
    scrap = scrap_me(url)

    try:
        title = scrap.title()[0],
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
        picture_link = scrap.picture()[0]
    except AttributeError:
        picture_link = None

    return {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions,
        'picture_link': picture_link,
    }

def get_all_recipes(page_num):
    # some sites close their content for 'bots', so user-agent must be supplied
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    }
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


def main(start_page=1, num_pages=1916, status_interval=50):
    recipes_epi = {}

    start = time.time()
    for i in range(start_page, num_pages + start_page):
        recipes_epi.update(get_all_recipes(i))
        if i % status_interval == 0:
            print('Scraping page {} of {}'.format(i + 1 - start_page, num_pages))
    print('Scraped {} recipes from {} in {:.0f} minutes'.format(
        len(recipes_epi), base_url, (time.time() - start) / 60))

    # Save to disk as JSON
    with open('recipes_raw.json', 'w') as f:
        json.dump(recipes_epi, f)

if __name__ == '__main__':
    main(status_interval=1)
