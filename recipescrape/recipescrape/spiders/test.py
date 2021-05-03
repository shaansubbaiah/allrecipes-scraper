import re
data = {
    "name": "Chocolate Chocolate Chip Cookies I",
    "url": "https://www.allrecipes.com/recipe/9827/chocolate-chocolate-chip-cookies-i/",
    "author": "KATHY",
    "summary": "These cookies are great...you get a double dose of chocolate! My kids love them.",
    "rating": "4.72",
    "rating_count": "4140",
    "review_count": "3099",
    "ingredients": [
        "1 cup butter, softened ",
        "1\u2009\u00bd cups white sugar ",
        "2  eggs ",
        "2 teaspoons vanilla extract ",
        "2 cups all-purpose flour ",
        "\u2154 cup cocoa powder ",
        "\u00be teaspoon baking soda ",
        "\u00bc teaspoon salt ",
        "2 cups semisweet chocolate chips ",
        "\u00bd cup chopped walnuts  (Optional)"
    ],
    "directions": [
        "Preheat oven to 350 degrees F (175 degrees C).",
        "In large bowl, beat butter, sugar, eggs, and vanilla until light and fluffy. Combine the flour, cocoa, baking soda, and salt; stir into the butter mixture until well blended. Mix in the chocolate chips and walnuts. Drop by rounded teaspoonfuls onto ungreased cookie sheets.",
        "Bake for 8 to 10 minutes in the preheated oven, or just until set. Cool slightly on the cookie sheets before transferring to wire racks to cool completely."
    ],
    "prep": "15 mins",
    "cook": "10 mins",
    "total": "20 mins",
    "servings": "45 mins",
    "yield": "48",
    "calories": "124.7",
    "nutrients": {
        "protein:": "1.5g",
        "carbohydrates:": "15.5g",
        "dietary fiber:": "1g",
        "sugars:": "10.2g",
        "fat:": "7.1g",
        "saturated fat:": "3.9g",
        "cholesterol:": "17.9mg",
        "vitamin a iu:": "128.6IU",
        "niacin equivalents:": "0.7mg",
        "folate:": "13.1mcg",
        "calcium:": "mg",
        "iron:": "0.7mg",
        "magnesium:": "17.2mg",
        "potassium:": "70.8mg",
        "sodium:": "63.1mg",
        "thiamin:": "0.1mg",
        "calories from fat:": "64.3"
    }
}


x = data["nutrients"].values()
print(x)
print(type(x))
for nutrient in x:
    try:
        val = float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', nutrient)[0])
    except:
        val = 0.0
    print(val)

x = data["nutrients"]
print(x)
for nutrient in x:
    # try:
    #     val = float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', nutrient)[0])
    # except:
    #     val = 0.0
    # print(val)
    print(re.findall(r'[a-zA-Z]+$', x[nutrient]))

# zip()
