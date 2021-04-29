import scrapy

class RecipeSpider(scrapy.Spider):
    name = "recipe"

    start_urls = [
        'https://www.allrecipes.com/recipe/235158/worlds-best-honey-garlic-pork-chops/',
        'https://www.allrecipes.com/recipe/283870/easy-grilled-corn-salad/'
    ]

    def parse(self, response):
        
        rating = response.css('.review-star-text::text').get()
        if 'Unrated' in rating:
            rating = '-1'
        else:
            rating = rating.replace('Rating:', '').replace('stars', '').strip()
    
        rating_count = response.css('.ratings-count::text').get()
        if rating_count is not None:
            rating_count = rating_count.replace('\\n', '').replace('Ratings', '').strip()
        else:
            rating_count = '0'

        review_count = response.css('.review-headline-count::text').get()
        if review_count is not None:
            review_count = review_count.strip()[1:-1]
        else:
            review_count = '0'
        
        nutrients_list = {}
        nutrients = response.css('.nutrition-body .nutrition-row')
        for nutrient in nutrients:
            nutrient_name = nutrient.css('.nutrient-name::text').get().replace('\\n', '').strip()
            nutrient_value = nutrient.css('.nutrient-value::text').get().replace('\\n', '').strip()
            nutrients_list[nutrient_name] = nutrient_value
        
        yield {
            'name': response.css('h1.headline.heading-content::text').get(),
            'url': response.url,
            'author': response.css('.author-name-title .authorName::text').get(),
            'summary': response.css('.recipe-summary p::text').get(),
            'rating': rating,
            'rating_count': rating_count,
            'review_count': review_count,
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
