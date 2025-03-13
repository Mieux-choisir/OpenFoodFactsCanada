import re
import unicodedata


class CategoryCreator:

    def create_categories(self, file_path: str) -> dict:
        off_categories = {}
        last_added = None

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("en: "):
                    categories_line_list = self.__normalize_line("en", line)
                    off_categories[categories_line_list[0]] = categories_line_list
                    last_added = categories_line_list[0]

                elif re.compile("..:").match(line):
                    categories_line_list = self.__normalize_line(line[:2], line)
                    if last_added is None:
                        off_categories[categories_line_list[0]] = categories_line_list
                        last_added = categories_line_list[0]
                    else:
                        for cat in categories_line_list:
                            off_categories[last_added].append(cat)

                elif line.strip() == "":
                    last_added = None

        return off_categories

    def __normalize_line(self, language_code, line):
        return [
            language_code + ":" + self.__normalize_string(x)
            for x in line[3:].split(",")
        ]

    @staticmethod
    def __normalize_string(given_string):
        given_string = given_string.lower().strip().replace(" ", "-")
        given_string = given_string.replace('\'', '-')
        given_string = given_string.replace('’', '-')
        given_string = given_string.replace('.', '-')

        normalized_string = unicodedata.normalize('NFKD', given_string)
        formatted_string = ''.join([c for c in normalized_string if not unicodedata.combining(c)])

        return formatted_string
