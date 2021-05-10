<div align="center">
<h1> AllRecipes Scraper 🥗</h1>
Scrapy spider to scrape recipe and nutritional data from <code>www.allrecipes.com</code>. <strong>35,516 recipes</strong> scraped, found in <code>/export</code>. 
<br>
Data was used to provide insight of the nutritional value of various recipes.
</div>

<br>

Data scraped for each recipe includes:

```python
# Recipe and related information 
'name', 'url', 'category', 'author', 'summary', 'rating', 'rating_count', 'review_count', 'ingredients', 'directions', 'prep', 'cook', 'total', 'Servings', 'Yield', 
# Nutritional information
'calories', 'carbohydrates_g', 'sugars_g', 'fat_g', 'saturated_fat_g', 'cholesterol_mg', 'protein_g', 'dietary_fiber_g', 'sodium_mg', 'calories_from_fat',
# Additional nutritional info - Metals
'calcium_mg', 'iron_mg', 'magnesium_mg', 'potassium_mg', 'zinc_mg', 'phosphorus_mg',
# Additional nutritional info - Vitamins
'vitamin_a_iu_IU', 'niacin_equivalents_mg', 'vitamin_b6_mg', 'vitamin_c_mg', 'folate_mcg', 'thiamin_mg', 'riboflavin_mg', 'vitamin_e_iu_IU', 'vitamin_k_mcg', 'biotin_mcg', 'vitamin_b12_mcg',
# Additional nutritional info - Fats
'mono_fat_g', 'poly_fat_g', 'trans_fatty_acid_g', 'omega_3_fatty_acid_g', 'omega_6_fatty_acid_g'
```

> *Note:* Many recipes do not list most of the nutrients from the 'Additional nutritional info'. A few nutrients aren't scraped and have been omitted from 'Additional nutritional info' due to its listing being extremely scarce.

### Example data
```json
{
    "name":"Simple Macaroni and Cheese",
    "url":"https://www.allrecipes.com/recipe/238691/simple-macaroni-and-cheese/",
    "category":"main-dish",
    "author":"g0dluvsugly",
    "summary":"A very quick and easy fix to a tasty side-dish. Fancy, designer mac and cheese often costs forty or fifty dollars to prepare when you have so many exotic and expensive cheeses, but they aren't always the best tasting. This recipe is cheap and tasty.",
    "rating":4.42,
    "rating_count":834,
    "review_count":575,
    "ingredients":"1 (8 ounce) box elbow macaroni ; ¼ cup butter ; ¼ cup all-purpose flour ; ½ teaspoon salt ;   ground black pepper to taste ; 2 cups milk ; 2 cups shredded Cheddar cheese",
    "directions":"Bring a large pot of lightly salted water to a boil. Cook elbow macaroni in the boiling water, stirring occasionally until cooked through but firm to the bite, 8 minutes. Drain. Melt butter in a saucepan over medium heat; stir in flour, salt, and pepper until smooth, about 5 minutes. Slowly pour milk into butter-flour mixture while continuously stirring until mixture is smooth and bubbling, about 5 minutes. Add Cheddar cheese to milk mixture and stir until cheese is melted, 2 to 4 minutes. Fold macaroni into cheese sauce until coated.",
    "prep":"10 mins",
    "cook":"20 mins",
    "total":"30 mins",
    "servings":"4",
    "yield":"4 servings",
    "calories":630.2,
    "carbohydrates_g":55.0,
    "sugars_g":7.6,
    "fat_g":33.6,
    "saturated_fat_g":20.9,
    "cholesterol_mg":99.6,
    "protein_g":26.5,
    "dietary_fiber_g":2.1,
    "sodium_mg":777.0,
    "calories_from_fat":302.2,
    "calcium_mg":567.9,
    "iron_mg":2.7,
    "magnesium_mg":61.8,
    "potassium_mg":380.0,
    "vitamin_a_iu_IU":1152.0,
    "niacin_equivalents_mg":10.1,
    "vitamin_c_mg":0.3,
    "folate_mcg":165.6,
    "thiamin_mg":0.7
}
```


## Run
First run `pip install scrapy`
### Run the spider:

- Set `DEBUG = False` in `recipescrape/spiders/recipes.py`
- Run `scrapy crawl recipes`

### Run the spider w/ minimal logs with count of items scraped and pause/resume-ability:

- Set `DEBUG = True` in `recipescrape/spiders/recipes.py`
- Run `scrapy crawl recipes -L WARN --logfile=scrapelog.txt -s JOBDIR=recipes/spider-1`

## Extras

### Spider to extract all the nutrient names:

- Run `pip install pandas`
- Make sure `DEBUG = True` in `nutrient_list.py`
- Run `scrapy crawl nutrients -o nutrients.csv -L WARN -s JOBDIR=nutrients/spider-1`
- Outputs 'items_count', 'nutri_count', 'nutri_list', 'url' in `nutrients.csv` in which the last row contains the unified list of nutritients found so far.

### Combine CSV files generated

- There are many ways to combine CSV files, a sample python file `/extras/combine_csv.py` is included for quick reference
