from domain.utils.category_creator import CategoryCreator


class CategoryMapper:

    def __init__(self, category_creator: CategoryCreator):
        self.off_categories: dict = category_creator.create_off_categories(
            "../categories_taxonomy.txt"
        )
        self.fdc_to_off_categories: dict = (
            category_creator.create_fdc_to_off_categories_mapping(
                "../categories_mapping_fdc_off.json", self.off_categories
            )
        )

    def get_off_category_of_off_product(self, given_categories: str) -> str:
        given_categories_list = list(
            filter(None, map(str.strip, given_categories.split(",")))
        )
        given_categories_list.reverse()
        off_category = "en:other"

        found = False
        for given_category in given_categories_list:
            for key, value_list in self.off_categories.items():
                if given_category in value_list:
                    off_category = key
                    found = True
                    break

            if found:
                break

        return off_category

    def get_off_category_of_fdc_product(self, given_category: str) -> list[str]:
        off_categories = []

        given_off_categories = self.fdc_to_off_categories.get(given_category)
        if given_off_categories is not None:
            for searched_category in given_off_categories:
                for key, value_list in self.off_categories.items():
                    if searched_category in value_list:
                        off_categories.append(key)
                        break

        if not off_categories:
            off_categories = [
                given_category.strip()
                .lower()
                .replace(",", "")
                .replace("&", "")
                .replace(" ", "-")
                + "-fdc"
            ]

        return off_categories
