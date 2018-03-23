# Recipe box

Recipe box scrapes recipes from food websites. The following websites are currently supported (Python 3):

* [Foodnetwork.com](http://www.foodnetwork.com/)
* [Epicurious.com](http://www.epicurious.com/)
* [Allrecipes.com](http://allrecipes.com/)

Please note that web scraping may be prohibited under the terms of use, and I recommend adhering the terms of use of each website.

## Usage

### Scrape recipe contents
* `$ python src/get_recipes.py --fn --multi`
* `$ python src/get_recipes.py --epi --multi`
* `$ python src/get_recipes.py --ar --sleep 200`

### Download pictures
* `$ python src/get_pictures.py --filename "recipes_raw_fn.json"`
* `$ python src/get_pictures.py --filename "recipes_raw_epi.json"`
* `$ python src/get_pictures.py --filename "recipes_raw_ar.json"`
