class CategoryCreator:

    @staticmethod
    def create_categories(file_path: str) -> dict:
        en_categories = {}

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("en: "):
                    categories_line_list = ["en:"+x.lower().strip().replace(" ", "-") for x in line[3:].split(',')]
                    en_categories[categories_line_list[0]] = categories_line_list

        return en_categories
