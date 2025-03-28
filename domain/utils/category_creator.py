import re

import ijson
import unicodedata


class CategoryCreator:

    def create_off_categories(self, file_path: str) -> dict:
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
        mapping = self.__get_mapping_from_file(file_path)
        mapping = self.__remove_absent_off_categories(mapping, off_categories)

        return mapping

    def __normalize_line(self, language_code, line):
        return [
            language_code + ":" + self.__normalize_string(x)
            for x in re.sub(r"^([a-zA-Z][a-zA-Z]): *", r"", line, flags=re.M).split(",")
        ]

    @staticmethod
    def __normalize_string(given_string):
        given_string = given_string.lower().strip()
        given_string = given_string.replace(" ", "-")
        given_string = given_string.replace("'", "-")
        given_string = given_string.replace("’", "-")
        given_string = given_string.replace(".", "-")

        normalized_string = unicodedata.normalize("NFKD", given_string)
        formatted_string = "".join(
            [c for c in normalized_string if not unicodedata.combining(c)]
        )

        return formatted_string

    @staticmethod
    def __get_mapping_from_file(file_path: str) -> dict:
        mapping = {}

        with open(file_path, "r", encoding="utf-8") as file:
            for obj in ijson.items(file, "categories.item"):
                matching_categories = obj.get("off")
                if matching_categories is not None:
                    mapping[obj.get("fdc")] = [
                        (x.strip().lower().replace("en: ", "en:", 1).replace(" ", "-"))
                        for x in matching_categories
                    ]

        return mapping

    def __remove_absent_off_categories(self, mapping: dict, categories: dict) -> dict:
        for mapping_key, mapping_values in mapping.items():
            for value in mapping_values:
                if self.__is_absent(value, categories):
                    mapping[mapping_key].remove(value)
        return mapping

    @staticmethod
    def __is_absent(searched_value: str, categories: dict):
        found = False
        for key, value in categories.items():
            if searched_value in value.get("values"):
                found = True
                break

        return not found
