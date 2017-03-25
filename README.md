# Recipe box

Scrape sets of recipes from food websites. Currently supports three websites in Python 3:

* [Foodnetwork.com](http://www.foodnetwork.com/)
* [Epicurious.com](http://www.epicurious.com/)
* [Allrecipes.com](http://allrecipes.com/)

## Usage

### Scrape recipe contents
* `$ python src/get_recipes.py --fn --multi`
* `$ python src/get_recipes.py --epi --multi`
* `$ python src/get_recipes.py --ar --sleep 200`

### Download pictures
* `$ python src/get_pictures.py --filename "recipes_raw_fn.json"`
* `$ python src/get_pictures.py --filename "recipes_raw_epi.json"`
* `$ python src/get_pictures.py --filename "recipes_raw_ar.json"`
