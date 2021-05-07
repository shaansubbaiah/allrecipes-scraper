import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = True
FIELDS = [
    # Recipe and related information
    'name', 'url', 'category', 'author', 'summary', 'rating', 'rating_count', 'review_count', 'ingredients', 'directions', 'prep', 'cook', 'total', 'servings', 'yield',
    # Nutritional information
    'calories', 'carbohydrates_g', 'sugars_g', 'fat_g', 'saturated_fat_g', 'cholesterol_mg', 'protein_g', 'dietary_fiber_g', 'sodium_mg', 'calories_from_fat',
    # Additional nutritional info - Metals
    'calcium_mg', 'iron_mg', 'magnesium_mg', 'potassium_mg', 'zinc_mg', 'phosphorus_mg',
    # Additional nutritional info - Vitamins
    'vitamin_a_iu_IU', 'niacin_equivalents_mg', 'vitamin_b6_mg', 'vitamin_c_mg', 'folate_mcg', 'thiamin_mg', 'riboflavin_mg', 'vitamin_e_iu_IU', 'vitamin_k_mcg', 'biotin_mcg', 'vitamin_b12_mcg',
    # Additional nutritional info - Fats
    'mono_fat_g', 'poly_fat_g', 'trans_fatty_acid_g', 'omega_3_fatty_acid_g', 'omega_6_fatty_acid_g'
]


def getFloat(x, index=0):
    # extracts only the numerical portion of text
    try:
        return float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', x)[index])
    except:
        return 0.0


def getText(x, index=0, toLower=False):
    # extracts only the alphabetical portion of text
    try:
        tmp = re.findall(r'[a-zA-Z_]+', x)[index]
        if toLower:
            return tmp.lower()
        return tmp

    except:
        return ''


def delSpaces(x):
    # strips and removes annoying carriage returns
    return x.translate({ord(c): None for c in u'\r\n\t'}).strip()


class RecipeSpider(CrawlSpider):
    name = 'recipes'
    allowed_domains = ['allrecipes.com']

    start_urls = ['https://www.allrecipes.com/recipes/?page=2']

    custom_settings = {
        'FEED_EXPORT_FIELDS': FIELDS,
        'FEEDS': {
            './export/recipes.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf8',
            },
            './export/recipes.csv': {
                'format': 'csv'
            },
        }
    }

    rule_next = Rule(LinkExtractor(restrict_css='.category-page-list-related-nav-next-button'),
                     follow=True,
                     )

    rule_recipe = Rule(LinkExtractor(allow=(r'.+\/recipe\/.+\/$'), unique=True),
                       callback='parse_item',
                       follow=True,
                       )

    rules = (rule_recipe, rule_next)

    def parse_item(self, response):

        if DEBUG:
            self.state['items_count'] = self.state.get('items_count', 0) + 1
            self.log(
                f"{self.state['items_count']} {response.url}", logging.WARN)

        # extract category from breadcrumb url
        breadcrumb_links = response.css(
            '.breadcrumbs__link::attr(href)').getall()
        try:
            category = breadcrumb_links[2].split('/')[-2]
        except:
            category = 'uncategorized'

        rating = getFloat(response.css('.review-star-text::text').get())

        rating_count = int(
            getFloat(response.css('.ratings-count::text').get()))

        review_count = int(getFloat(response.css(
            '.review-headline-count::text').get()))

        # recipe meta -> 'prep', 'cook', 'total', 'servings', 'yield'
        recipe_meta = {}
        recipe_meta_headers = response.css(
            '.recipe-meta-item-header::text').getall()
        recipe_meta_bodies = response.css(
            '.recipe-meta-item-body::text').getall()
        for (h, b) in zip(recipe_meta_headers, recipe_meta_bodies):
            h = getText(h, toLower=True)
            b = delSpaces(b)
            recipe_meta[h] = b

        nutrients_list = {}
        nutrients = response.css('.nutrition-body .nutrition-row')
        for nutrient in nutrients:
            n_name = delSpaces(nutrient.css('.nutrient-name::text').get())
            n_name = getText(n_name.replace(' ', '_'))

            # get the numerical quantity of nutrient
            n_value = getFloat(nutrient.css('.nutrient-value::text').get())

            # append unit to the nutrient name
            n_unit = getText(nutrient.css('.nutrient-value::text').get())
            if n_unit != '':
                n_name += "_" + n_unit

            nutrients_list[n_name] = n_value

        nutrients_list['calories'] = getFloat(response.css(
            '.nutrition-top::text').getall()[2])

        data = {
            'name': response.css('h1.headline.heading-content::text').get(),
            'url': response.url,
            'category': category,
            'author': response.css('.author-name-title .authorName::text').get(),
            'summary': delSpaces(response.css('.recipe-summary p::text').get()),
            'rating': rating,
            'rating_count': rating_count,
            'review_count': review_count,
            'ingredients': delSpaces('; '.join(response.css('.ingredients-item-name::text').getall())),
            'directions': delSpaces(' '.join(response.css('.instructions-section-item p::text').getall()))
        }

        # combine the 3 dictionaries
        data = data | recipe_meta | nutrients_list

        yield data
