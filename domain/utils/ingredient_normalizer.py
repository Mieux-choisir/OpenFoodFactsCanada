import re


class IngredientNormalizer:
    def normalise_ingredients_list(self, ingredients_text: str) -> list[str]:
        """Creates a normalised ingredients list based on a given text of ingredients.
        ingredients_text is an enumeration of the ingredients separated by a comma"""
        ingredients_text = ingredients_text.title()
        ingredients_text = self.__remove_unnecessary_text(ingredients_text)
        ingredients_list = self.__segment_ingredients(ingredients_text)
        ingredients_list = self.__clean_ingredients(ingredients_list)
        ingredients_list = self.__remove_repetitions(ingredients_list)

        return ingredients_list

    @staticmethod
    def __remove_unnecessary_text(ingredients_text: str) -> str:
        """Removes text that is not essential information about the ingredients (e.g. "contains", ".", etc.)"""
        cleaned_text = re.sub(
            r"contains.*?of", "contains of", ingredients_text, flags=re.IGNORECASE
        )
        cleaned_text = cleaned_text.replace(".", ",")
        return cleaned_text.strip()

    @staticmethod
    def __segment_ingredients(ingredients_text: str) -> list[str]:
        """Splits the text by commas, excluding the ones between '(' or '[' and ']' or ')'"""
        if ingredients_text.endswith(","):
            ingredients_text = ingredients_text[:-1]

        pattern = r"[^,()\[\]]+(?:\([^\(\)]*\))?(?:\[[^\[\]]*\])?"
        ingredients_list = re.findall(pattern, ingredients_text)

        return ingredients_list

    @staticmethod
    def __clean_ingredients(ingredients_list: list[str]) -> list[str]:
        """Removes everything before the last appearing colon for each ingredient in the list"""
        cleaned_ingredients_list = []
        for ingredient in ingredients_list:
            ingredient = ingredient.strip()
            ingredient = re.sub(r".*:(.*)", r"\1", ingredient).strip()
            cleaned_ingredients_list.append(ingredient)

        return cleaned_ingredients_list

    @staticmethod
    def __remove_repetitions(ingredients_list: list[str]) -> list[str]:
        """Removes repetitions in the list while keeping the order of the first occurrences"""
        seen = set()
        simplified_ingredients_list = []
        for item in ingredients_list:
            if item not in seen:
                simplified_ingredients_list.append(item)
                seen.add(item)

        return simplified_ingredients_list
