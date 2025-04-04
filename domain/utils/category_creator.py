import re

import ijson
import unicodedata


class CategoryCreator:
    """
    This is a class that creates the Open Food Facts categories from given files.

    Methods:
        create_off_categories(file_path): Creates a mapping of OFF categories based on the taxonomy in the given file
        create_fdc_to_off_categories_mapping(file_path, off_categories): Creates a mapping of FDC to OFF categories based on the
        mapping in the given file and on the given OFF categories
    """

    def create_off_categories(self, file_path: str) -> dict:
        """Creates a mapping of OFF categories based on its taxonomy, where:
        - each key is the canonical term of a category
        - each value is a dictionary with:
            - values: the list of all the terms corresponding to the category
            - parents: the list of the immediate parents of the category"""
        off_categories = {}
        last_added = None
        parents = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped_line = line.strip()

                if stripped_line.startswith("< en:"):
                    parents.append(self.__normalize_string(stripped_line[2:]))

                elif re.compile("..:").match(stripped_line):
                    categories_line_list = self.__normalize_line(
                        stripped_line[:2], stripped_line
                    )

                    if last_added is None:
                        canonical_category = categories_line_list[0]
                        off_categories[canonical_category] = {
                            "values": categories_line_list,
                            "parents": parents,
                        }

                        last_added = canonical_category
                        parents = []

                    else:
                        for cat in categories_line_list:
                            off_categories[last_added]["values"].append(cat)

                elif stripped_line == "":
                    last_added = None
        return off_categories

    def create_fdc_to_off_categories_mapping(
        self, file_path: str, off_categories: dict
    ) -> dict:
        """Creates a dictionary that maps FDC categories to OFF categories, where:
        - each key is a FDC category
        - each value is the list of the corresponding OFF categories (canonical terms from the taxonomy)
        """
        mapping = self.__get_mapping_from_file(file_path)
        mapping = self.__remove_absent_off_categories(mapping, off_categories)

        return mapping

    def __normalize_line(self, language_code: str, line: str) -> list[str]:
        """Normalizes a category line, which can contain several terms. The result is a list where each element is a normalized term"""
        return [
            language_code + ":" + self.__normalize_string(x)
            for x in re.sub(r"^([a-zA-Z][a-zA-Z]): *", r"", line, flags=re.M).split(",")
        ]

    @staticmethod
    def __normalize_string(given_string: str) -> str:
        """Normalizes a given category term"""
        given_string = given_string.lower().strip()
        given_string = re.sub(r"[ '’.()]+", "-", given_string, flags=re.M)
        if given_string.startswith("-"):
            given_string = given_string[1:]
        if given_string.endswith("-"):
            given_string = given_string[:-1]

        normalized_string = unicodedata.normalize("NFKD", given_string)
        formatted_string = "".join(
            [c for c in normalized_string if not unicodedata.combining(c)]
        )

        return formatted_string

    def __get_mapping_from_file(self, file_path: str) -> dict:
        """Returns the mapping of FDC to OFF categories from a json file"""
        mapping = {}

        with open(file_path, "r", encoding="utf-8") as file:
            for obj in ijson.items(file, "categories.item"):
                matching_categories = obj.get("off")
                if matching_categories is not None:
                    mapping[obj.get("fdc")] = [
                        self.__format_category(x) for x in matching_categories
                    ]

        return mapping

    @staticmethod
    def __format_category(category):
        """Formats a given category"""
        category = category.strip().lower().replace("en: ", "en:", 1)

        category = re.sub(r"[ '’.()]+", "-", category, flags=re.M)
        if category.startswith("-"):
            category = category[1:]
        if category.endswith("-"):
            category = category[:-1]

        return category

    def __remove_absent_off_categories(self, mapping: dict, categories: dict) -> dict:
        """Removes OFF categories in the FDC-OFF mapping values if they are not present in the OFF categories dictionary"""
        for mapping_key, mapping_values in mapping.items():
            for value in mapping_values:
                if self.__is_absent(value, categories):
                    mapping[mapping_key].remove(value)
        return mapping

    @staticmethod
    def __is_absent(searched_value: str, categories: dict) -> bool:
        """Returns True if the searched value is absent in the given dictionary, False otherwise"""
        found = False
        for key, value in categories.items():
            if searched_value in value.get("values"):
                found = True
                break

        return not found
