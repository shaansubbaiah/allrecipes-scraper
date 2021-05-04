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


# x = "mg"


# try:
#     val = re.findall(r'[-+]?[0-9]*\.?[0-9]+', x)[0]
# except:
#     val = 0.0

# try:
#     unit = re.findall(r'[a-zA-Z]+$', x)[0]
# except:
#     unit = ""

# print(val)
# print(unit)


remove_escapes = {ord(c): None for c in u'\r\n\t'}
s = "Quick and easy recipe for roasted baby potatoes. Bake them at the same time as you cook your main dish!\n Can also be used as a quick appetizer!\n\n These were so good you don't even need butter or salt to taste. Made the mistake of having them done before the main dish and they were almost all gone by the time dinner started!"
print(s)
print(s.translate(remove_escapes))


# t = "https: // www.allrecipes.com/recipes/ https: // www.allrecipes.com/recipe/12254/graham-cracker-crust-i/ https: // www.allrecipes.com/recipe/7255/dirt-cake-i/ RegExr was created by gskinner.com, and is proudly hosted by Media Temple. Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & JavaScript flavors of RegEx are supported. Validate your expression with Tests mode. The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or favorite in My Patterns. Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English."
# print(re.findall(r'.+\/recipe\/.+', t))
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
