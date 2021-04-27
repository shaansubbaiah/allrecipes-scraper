from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import requests
import os
import re
from time import time as timer
import threading

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0")
options.add_argument('--headless')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=options)

USE_EXISTING_VALUES = True



def getCategoryLinks():

    if USE_EXISTING_VALUES:
        return ['https://www.allrecipes.com/recipes/88/bbq-grilling/', 'https://www.allrecipes.com/recipes/156/bread/', 'https://www.allrecipes.com/recipes/78/breakfast-and-brunch/', 'https://www.allrecipes.com/recipes/79/desserts/', 'https://www.allrecipes.com/recipes/17562/dinner/', 'https://www.allrecipes.com/recipes/1642/everyday-cooking/', 'https://www.allrecipes.com/recipes/84/healthy-recipes/', 'https://www.allrecipes.com/recipes/85/holidays-and-events/', 'https://www.allrecipes.com/recipes/17567/ingredients/', 'https://www.allrecipes.com/recipes/17561/lunch/', 'https://www.allrecipes.com/recipes/80/main-dish/', 'https://www.allrecipes.com/recipes/92/meat-and-poultry/', 'https://www.allrecipes.com/recipes/95/pasta-and-noodles/', 'https://www.allrecipes.com/recipes/96/salad/', 'https://www.allrecipes.com/recipes/93/seafood/', 'https://www.allrecipes.com/recipes/81/side-dish/', 'https://www.allrecipes.com/recipes/94/soups-stews-and-chili/', 'https://www.allrecipes.com/recipes/236/us-recipes/', 'https://www.allrecipes.com/recipes/86/world-cuisine/']

    categories = driver.find_elements_by_class_name('recipeCarousel__link')

    print(f'Found {len(categories)} categories.')

    category_links = []
    for category in categories:
        category_links.append(category.get_attribute('href'))

    return category_links



def getRecipeLinks(category_link):
    
    driver.get(category_link)

    recipe_links = []
    recipes = driver.find_elements_by_class_name('card__titleLink')
    for recipe in recipes:
        recipe_links.append(recipe.get_attribute('href'))

    print(recipe_links)

    return recipe_links



def scraper():
    driver.get('https://www.allrecipes.com/recipes/')

    category_links = getCategoryLinks()

    recipe_links = getRecipeLinks(category_links[0])

    driver.quit()



def screamErrorAndQuit(msg):
    print(f'ERROR: {msg}')
    driver.quit()
    exit(1)



scraper()

# categories - li.recipeCarousel__listItem:nth-child(1) > a:nth-child(1)
# html.wf-sourcesanspro-n7-active.wf-sourcesanspro-n6-active.wf-sourcesanspro-n4-active.wf-sourcesanspro-i4-active.wf-active body.template-aggregate.node-food.karma-site-container.alrcom main.container-full-width div.component.circular-carousel.category-page-topics.category-page-body div.component.circular-carousel.circularCarousel.recipeCarousel nav.carouselNav.circularCarousel__viewPort.recipeCarousel__viewPort div.carouselNav__listWrapper.recipeCarousel__listWrapper ul.carouselNav__list.recipeCarousel__list li.carouselNav__listItem.recipeCarousel__listItem a.carouselNav__link.recipeCarousel__link
