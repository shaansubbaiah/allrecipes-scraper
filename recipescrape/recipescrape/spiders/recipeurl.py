import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RecipeurlSpider(CrawlSpider):
    name = 'recipeurl'
    allowed_domains = ['allrecipes.com']
    start_urls = [
        # 'https://www.allrecipes.com/recipes/79/desserts/',
        'https://www.allrecipes.com/recipes/79/desserts/?page=2',
    ]

    rule_recipe = Rule(LinkExtractor(restrict_css='.tout__imageLink',
                allow=('recipe/')),
                callback='parse_item',
                follow=False,
                )
    
    rule_next = Rule(LinkExtractor(restrict_css='.category-page-list-related-nav-next-button'),
                follow=True,
                )

    rules = (
        rule_recipe,
        rule_next
    )

    count = 0

    def parse_item(self, response):
            
        # if 'gallery' in response.url:
        #     self.logger.info('GALLERY! %s', response.url)
        if self.count < 100:
            rating = response.css('.review-star-text::text').get()
            # Lowest a recipe can be rated is 1 star 
            if 'Unrated' in rating:
                rating = '0'
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

            try:
                prep = response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[0].replace('\\n', '').strip()
            except:
                prep = ''
            
            try:
                cook = response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[1].replace('\\n', '').strip()
            except:
                cook = ''
            
            try:
                total = response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[2].replace('\\n', '').strip()
            except:
                total = ''
            
            try:
                servings = response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[3].replace('\\n', '').strip()
            except:
                servings = ''
            
            try:
                yields = response.css('.recipe-meta-item .recipe-meta-item-body::text').getall()[4].replace('\\n', '').strip()
            except:
                yields = ''
            
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
                'summary': response.css('.recipe-summary p::text').get().strip(),
                'rating': rating,
                'rating_count': rating_count,
                'review_count': review_count,
                'ingredients': response.css('.ingredients-item-name::text').getall(),
                'directions': response.css('.instructions-section-item p::text').getall(),
                'prep': prep,
                'cook': cook,
                'total': total,
                'servings': servings,
                'yield': yields,
                'calories': response.css('.nutrition-top::text').getall()[2].strip(),
                'nutrients': nutrients_list
            }
