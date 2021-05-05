import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
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


class RecipeurlSpider(CrawlSpider):
    name = 'recipes'
    allowed_domains = ['allrecipes.com']

    start_urls = ['https://www.allrecipes.com/recipes/?page=2']

    custom_settings = {
        'FEED_EXPORT_FIELDS': FIELDS
    }

    rule_next = Rule(LinkExtractor(restrict_css='.category-page-list-related-nav-next-button'),
                     follow=True,
                     )

    rule_recipe = Rule(LinkExtractor(allow=(r'.+\/recipe\/.+\/$'), unique=True),
                       callback='parse_item',
                       follow=True,
                       )

    rules = (
        rule_recipe,
        rule_next
    )

    def parse_item(self, response):

        if DEBUG:
            self.state['items_count'] = self.state.get('items_count', 0) + 1
            self.log(
                f"{self.state['items_count']} {response.url}", logging.WARN)

        breadcrumb_links = response.css(
            '.breadcrumbs__link::attr(href)').getall()
        try:
            category = breadcrumb_links[2].split('/')[-2]
        except:
            category = 'uncategorized'

        rating = response.css('.review-star-text::text').get()
        # lowest a recipe can be rated is 1 star
        if 'Unrated' in rating:
            rating = 0.0
        else:
            rating = float(rating.replace(
                'Rating:', '').replace('stars', '').strip())

        # try:
        #     rating = re.findall(r'[-+]?[0-9]*\.?[0-9]+',
        #                         response.css('.review-star-text::text').get())[0]
        # except:
        #     rating = 0.0

        rating_count = response.css('.ratings-count::text').get()
        if rating_count is not None:
            rating_count = int(rating_count.replace(
                '\\n', '').replace('Ratings', '').strip())
        else:
            rating_count = 0

        review_count = response.css('.review-headline-count::text').get()
        if review_count is not None:
            review_count = int(review_count.strip()[1:-1])
        else:
            review_count = 0

        recipe_meta = {}
        recipe_meta_headers = response.css(
            '.recipe-meta-item-header::text').getall()
        recipe_meta_bodies = response.css(
            '.recipe-meta-item-body::text').getall()
        for (h, b) in zip(recipe_meta_headers, recipe_meta_bodies):
            recipe_meta[h[:-1].lower()] = b.replace('\\n', '').strip()

        nutrients_list = {}
        nutrients = response.css('.nutrition-body .nutrition-row')
        for nutrient in nutrients:
            nutrient_name = nutrient.css(
                '.nutrient-name::text').get().replace('\\n', '').strip().replace(' ', '_')[:-1]

            nutrient_value = nutrient.css(
                '.nutrient-value::text').get().replace('\\n', '').strip()

            # get the numerical quantity of nutrient
            try:
                value = re.findall(
                    r'[-+]?[0-9]*\.?[0-9]+', nutrient_value)[0]
            except:
                value = 0.0

            # append unit to the nutrient name
            try:
                unit = re.findall(r'[a-zA-Z]+$', nutrient_value)[0]
            except:
                pass
            else:
                nutrient_name = nutrient_name + "_" + unit

            nutrients_list[nutrient_name] = float(value)

        try:
            nutrients_list['calories'] = float(response.css(
                '.nutrition-top::text').getall()[2].strip())
        except:
            pass

        remove_escapes = {ord(c): None for c in u'\r\n\t'}

        data = {
            'name': response.css('h1.headline.heading-content::text').get(),
            'url': response.url,
            'category': category,
            'author': response.css('.author-name-title .authorName::text').get(),
            'summary': response.css('.recipe-summary p::text').get().strip().translate(remove_escapes),
            'rating': rating,
            'rating_count': rating_count,
            'review_count': review_count,
            'ingredients': '; '.join(response.css('.ingredients-item-name::text').getall()).translate(remove_escapes),
            'directions': ' '.join(response.css('.instructions-section-item p::text').getall()).translate(remove_escapes)
        }

        # combine the 3 dictionaries
        data = data | recipe_meta | nutrients_list

        yield data
