import re

categories_aliments_base = {
    "en:flours": True,
    "en:rices": True,
    "en:pastas": True,
    "en:breads": True,
    "en:legumes": True,
    "en:eggs": True,
    "en:milks": True,
    "en:plain-yogurts": True,
    "en:vegetables": True,
    "en:fruits": True,
    "en:nuts": True,
    "en:seeds": True,
}

categories_non_base = {
    "en:snacks": True,
    "en:beverages": True,
    "en:desserts": True,
    "en:candies": True,
    "en:chocolates": True,
    "en:breakfast-cereals": True,
    "en:processed-meats": True,
}


def map_letter_to_number(letter: str) -> int | None:
    try:
        return ord(letter.lower()) - 96
    except TypeError:
        return None


def normalise_ingredients_list(ingredients_text: str) -> list[str]:
    """Creates a normalised ingredients list based on a given text of ingredients.
    ingredients_text is an enumeration of the ingredients separated by a comma"""
    # Step 1: Make each word start by a cap and the rest lowercase
    ingredients_text = ingredients_text.title()

    # Step 2: Split by commas
    if ingredients_text.endswith('.') or ingredients_text.endswith(','):
        ingredients_text = ingredients_text[:-1]
    ingredients_list = ingredients_text.split(',')

    # Step 3: Process each segment using regex
    cleaned_ingredients = [] #TODO the ingredients listed between ( ) are separated when they shouldn't be
    for ingredient in ingredients_list:
        # Use regex to match everything after the last colon
        ingredient = re.sub(r'.*:(.*)', r'\1', ingredient).strip()
        cleaned_ingredients.append(ingredient)

    # Step 4: Remove repetitions while keeping the order of the first occurrences
    seen = set()
    result = []
    for item in cleaned_ingredients:
        if item not in seen:
            result.append(item)
            seen.add(item)

    return result


def check_nova_raw_group(nova_group: str) -> bool:
    """Checks if the given nova group string is valid and returns True if it is a group of raw foods, False otherwise"""
    if nova_group and nova_group != "":
        try:
            nova_value = int(nova_group)
            if nova_value == 1:
                return True
            return False
        except ValueError:
            raise ValueError
    return False


def check_nova_transformed_group(nova_group: str) -> bool:
    """Checks if the given nova group string is valid and returns True if it is a group of ultra transformed foods,
    False otherwise"""
    if nova_group and nova_group != "":
        try:
            nova_value = int(nova_group)
            if nova_value == 4:
                return True
            return False
        except ValueError:
            raise ValueError
    return False


def check_pnn_groups(pnn: str):
    """Returns True if the given pnn group is either cereals or legumes, False otherwise"""
    if pnn in ["cereals", "legumes"]:
        return True
    return False


def check_string_categories(category: str):
    """Returns True if the given category is a foundation food AND not a non foundation food, False otherwise"""
    if category:
        categories = set(category.split(","))
        if any(cat in categories_aliments_base for cat in categories):
            if not any(cat in categories_non_base for cat in categories):
                return True
    return False


def check_list_categories(category: list):
    """Returns True if the given category is a foundation food AND not a non foundation food, False otherwise"""
    if (category and any(cat in categories_aliments_base for cat in category)
            and not any(cat in categories_non_base for cat in category)):
        return True
    return False


def check_additives(additives: str, nova_group: str) -> bool:
    """Returns True if there are no additives and the nova group is less than or equal to 2, False otherwise"""
    if additives and additives != "":
        try:
            if (
                    int(additives) == 0
                    and nova_group
                    and nova_group != ""
                    and int(nova_group) <= 2
            ):
                return True
        except ValueError:
            raise ValueError
    return False
