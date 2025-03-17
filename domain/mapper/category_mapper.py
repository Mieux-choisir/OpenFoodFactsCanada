from domain.utils.category_creator import CategoryCreator


class CategoryMapper:

    def __init__(self):
        self.off_categories: dict = CategoryCreator().create_categories(
            "../categories_taxonomy.txt"
        )
        self.fdc_to_off_categories: dict = CategoryCreator.create_fdc_to_off_mapping(
            "../categories_mapping_fdc_off.json"
        )

    def get_off_category_of_off_product(self, given_categories: str) -> str:
        given_categories_list = list(
            filter(None, map(str.strip, given_categories.split(",")))
        )
        given_categories_list.reverse()
        off_category = "en:other"
        for given_category in given_categories_list:
            found = False
            for key, value_list in self.off_categories.items():
                if given_category in value_list:
                    off_category = key
                    found = True
                    break
            if found:
                break

        return off_category

    def get_off_category_of_fdc_product(self, given_category: str) -> list[str]:
        off_category = []
        categories = self.fdc_to_off_categories.get(given_category)
        if categories is not None:
            off_category = self.fdc_to_off_categories.get(given_category)
        return off_category
