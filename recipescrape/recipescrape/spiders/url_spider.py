import scrapy


class UrlSpider(scrapy.Spider):
    name = "urls"

    start_urls = [
        'https://www.allrecipes.com/recipes/79/desserts/',
        # 'https://www.allrecipes.com/recipes/96/salad/'
    ]

    def parse(self, response):

        found_urls = response.css('.recipeCard__detailsContainer .card__titleLink::attr(href)').getall()
        
        urls = []

        for url in found_urls:
            if '/recipe/' in url:
                urls.append(url)

        yield {
            'urls' : urls
            # card__titleLink manual-link-behavior
        }
