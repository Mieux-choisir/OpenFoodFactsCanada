from domain.utils.category_creator import CategoryCreator


class FoodCategoryModel:

    def __init__(self):
        self.categories: list[str] = CategoryCreator.create_categories("../categories_taxonomy.txt")

    def get_off_category(self, given_categories: str) -> str:
        given_categories_list = list(filter(None, map(str.strip, given_categories.split(","))))
        given_categories_list.reverse()
        off_category = "en:other"
        for given_category in given_categories_list:
            found = False
            for key, value_list in self.categories.items():
                if given_category in value_list:
                    off_category = key
                    found = True
                    break
            if found:
                break

        return off_category
