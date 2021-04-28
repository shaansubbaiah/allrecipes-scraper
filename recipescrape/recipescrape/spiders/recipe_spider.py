import scrapy

class RecipeSpider(scrapy.Spider):
    name = "recipe"

    start_urls = [
        'https://www.allrecipes.com/recipe/235158/worlds-best-honey-garlic-pork-chops/'
    ]

    def parse(self, response):
        
        nutrients_list = {}
        nutrients = response.css('.nutrition-body .nutrition-row')
        for nutrient in nutrients:
            nutrients_list[nutrient.css('.nutrient-name::text').get().replace('\\n', '').strip()] = nutrient.css('.nutrient-value::text').get().replace('\\n', '').strip()

        
        yield {
            'name': response.css('h1.headline.heading-content::text').get(),
            'ratings': response.css('.ratings-count::text').get().replace('\\n', '').replace('Ratings', '').strip(),
            'reviews': response.css('.review-headline-count::text').get().strip()[1:-1],
            'url': response.url,
            'ingredients': response.css('.ingredients-item-name::text').getall(),
            'directions': response.css('.instructions-section-item p::text').getall(),
            'prep': response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[0].replace('\\n', '').strip(),
            'cook': response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[1].replace('\\n', '').strip(),
            'total': response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[2].replace('\\n', '').strip(),
            'servings': response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[3].replace('\\n', '').strip(),
            'yield': response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[4].replace('\\n', '').strip(),
            'calories': response.css('.nutrition-top::text').getall()[2].strip(),
            'nutrients': nutrients_list
        }
