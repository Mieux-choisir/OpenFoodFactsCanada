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
    ingredients_text = ingredients_text.title()
    ingredients_text = remove_unnecessary_text(ingredients_text)
    ingredients_list = segment_ingredients(ingredients_text)
    ingredients_list = clean_ingredients(ingredients_list)
    ingredients_list = remove_repetitions(ingredients_list)

    return ingredients_list


def remove_unnecessary_text(ingredients_text: str) -> str:
    """Removes text that is not essential information about the ingredients (e.g. "contains", ".", etc.)"""
    cleaned_text = re.sub(r'contains.*?of', 'contains of', ingredients_text, flags=re.IGNORECASE)
    cleaned_text = cleaned_text.replace('.', ',')
    return cleaned_text.strip()


def segment_ingredients(ingredients_text: str) -> list[str]:
    """Splits the text by commas, excluding the ones between '(' or '[' and ']' or ')'"""
    if ingredients_text.endswith(','):
        ingredients_text = ingredients_text[:-1]

    pattern = r'[^,()\[\]]+(?:\([^\(\)]*\))?(?:\[[^\[\]]*\])?'
    ingredients_list = re.findall(pattern, ingredients_text)

    return ingredients_list


def clean_ingredients(ingredients_list: list[str]) -> list[str]:
    """Removes everything before the last appearing colon for each ingredient in the list"""
    cleaned_ingredients_list = []
    for ingredient in ingredients_list:
        ingredient = ingredient.strip()
        ingredient = re.sub(r'.*:(.*)', r'\1', ingredient).strip()
        cleaned_ingredients_list.append(ingredient)

    return cleaned_ingredients_list


def remove_repetitions(ingredients_list: list[str]) -> list[str]:
    """Removes repetitions in the list while keeping the order of the first occurrences"""
    seen = set()
    simplified_ingredients_list = []
    for item in ingredients_list:
        if item not in seen:
            simplified_ingredients_list.append(item)
            seen.add(item)

    return simplified_ingredients_list


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


def check_pnn_groups(pnn: str) -> bool:
    """Returns True if the given pnn group is either cereals or legumes, False otherwise"""
    if pnn in ["cereals", "legumes"]:
        return True
    return False


def check_string_categories(category: str) -> bool:
    """Returns True if the given category is a foundation food AND not a non foundation food, False otherwise"""
    if category:
        categories = set(category.split(","))
        if any(cat in categories_aliments_base for cat in categories):
            if not any(cat in categories_non_base for cat in categories):
                return True
    return False


def check_list_categories(category: list) -> bool:
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
