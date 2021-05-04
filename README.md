# allrecipes-scraper

Data scraped for each recipe includes:

```python
[
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
]
```

> *Note:* Many recipes do not list most of the nutrients from the 'Additional nutritional info'. A few nutrients aren't scraped and have been omitted from 'Additional nutritional info' due to its listing being extremely scarce.

## Run

Run the spider:

`scrapy crawl recipes -o recipes.json -L WARN --logfile=scrapelog.txt -s JOBDIR=recipes/spider-1`

## Extras
Spider to extract all the nutrient names:
- Make sure `DEBUG = True` in `nutrient_list.py`
- Run `scrapy crawl nutrients -o nutrients.csv -L WARN -s JOBDIR=nutrients/spider-1`
- Outputs 'items_count', 'nutri_count', 'nutri_list', 'url' in `nutrients.csv` in which the last row contains the unified list of nutritients found so far.


<!-- https://www.health.harvard.edu/staying-healthy/listing_of_vitamins -->