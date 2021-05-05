import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = True


class RecipeurlSpider(CrawlSpider):
    name = 'nutrients'
    allowed_domains = ['allrecipes.com']

    start_urls = ['https://www.allrecipes.com/recipes/?page=2']

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
            self.state['nutri_count'] = self.state.get('nutri_count', 0) + 1
            self.state['nutri_list'] = self.state.get('nutri_list', [])

            self.log(
                f"C{self.state['items_count']} N{self.state['nutri_count']} {response.url}", logging.WARN)
            self.log(f"{self.state['nutri_count']}", logging.WARN)

        nutrients_list = ['calories']

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

            if float(value) > 0.0:
                nutrients_list.append(nutrient_name)

        for n in nutrients_list:
            if n not in self.state['nutri_list']:
                self.state['nutri_list'].append(n)
                self.state['nutri_count'] = len(self.state['nutri_list'])

        yield {
            'items_count': self.state['items_count'],
            'nutri_count': self.state['nutri_count'],
            'nutri_list': self.state['nutri_list'],
            'url': response.url
        }
