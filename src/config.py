from os import path, makedirs

path_src = path.dirname(path.abspath(__file__))
path_base = path.dirname(path_src)
path_data = path.join(path_base, 'data')
path_img = path.join(path_data, 'img')
path_scrapers = path.join(path_src, 'recipe-scraper')
path_outputs = path.join(path_base, 'outputs')

# verify paths exist otherwise make them
if not path.exists(path_outputs):
    makedirs(path_outputs)
if not path.exists(path_data):
    makedirs(path_data)
if not path.exists(path_img):
    makedirs(path_img)
