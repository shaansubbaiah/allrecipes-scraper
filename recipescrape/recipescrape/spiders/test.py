import re
data = {
    "name": "Graham Cracker Crust I",
    "url": "https://www.allrecipes.com/recipe/12254/graham-cracker-crust-i/",
    "author": "Carol",
    "summary": "This goes great with many pies.",
    "rating": 4.66,
    "rating_count": 1140,
    "review_count": 792,
    "ingredients": [
            "1\u2009\u00bd cups finely ground graham cracker crumbs ",
            "\u2153 cup white sugar ",
            "6 tablespoons butter, melted ",
            "\u00bd teaspoon ground cinnamon  (Optional)"
    ],
    "directions": [
        "Mix graham cracker crumbs, sugar, melted butter or margarine, and cinnamon until well blended . Press mixture into an 8 or 9 inch pie plate.",
        "Bake at 375 degrees F (190 degrees C) for 7 minutes.  Cool.  If recipe calls for unbaked pie shell, just chill for about 1 hour."
    ],
    "prep": "10 mins",
    "cook": "7 mins",
    "total": "17 mins",
    "Servings": "8",
    "Yield": "1 pie crust",
    "protein:": "1.2g",
    "carbohydrates:": "20.5g",
    "dietary fiber:": "0.5g",
    "sugars:": "13.2g",
    "fat:": "10.2g",
    "saturated fat:": "5.7g",
    "cholesterol:": "22.9mg",
    "vitamin a iu:": "266.9IU",
    "niacin equivalents:": "0.9mg",
    "folate:": "7.6mcg",
    "calcium:": "7.9mg",
    "iron:": "0.6mg",
    "magnesium:": "5mg",
    "potassium:": "24.6mg",
    "sodium:": "156.6mg",
    "calories from fat:": "92.1",
    "calories": "175.6"
}


x = "mg"


try:
    val = re.findall(r'[-+]?[0-9]*\.?[0-9]+', x)[0]
except:
    val = 0.0

try:
    unit = re.findall(r'[a-zA-Z]+$', x)[0]
except:
    unit = ""

print(val)
print(unit)

# x = data["nutrients"].values()
# print(x)
# print(type(x))
# for nutrient in x:
#     try:
#         val = float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', nutrient)[0])
#     except:
#         val = 0.0
#     print(val)

# x = data["nutrients"]
# print(x)
# for nutrient in x:
#     # try:
#     #     val = float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', nutrient)[0])
#     # except:
#     #     val = 0.0
#     # print(val)
#     print(re.findall(r'[a-zA-Z]+$', x[nutrient]))

# zip()
