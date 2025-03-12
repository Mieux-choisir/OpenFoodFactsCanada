import re


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

    @staticmethod
    def __normalize_line(language_code, line):
        return [
            language_code + ":" + x.lower().strip().replace(" ", "-")
            for x in line[3:].split(",")
        ]
        # TODO normalize by removing accents, replacing ' and ’, and eventually other special characters if necessary
