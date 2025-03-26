import re

from domain.utils.category_creator import CategoryCreator


class CategoryMapper:

    def __init__(
        self, category_creator: CategoryCreator, off_file: str, fdc_to_off_file: str
    ):
        self.file = off_file

        self.off_categories: dict = category_creator.create_off_categories(off_file)
        self.fdc_to_off_categories: dict = (
            category_creator.create_fdc_to_off_categories_mapping(
                fdc_to_off_file, self.off_categories
            )
        )

    def get_off_categories_of_off_product(self, given_categories: str) -> list[str]:
        given_categories_list = list(
            filter(None, map(str.strip, given_categories.split(",")))
        )
        given_categories_list.reverse()

        off_categories = self.__get_off_categories_from_given_categories(
            given_categories_list
        )
        if not off_categories:
            off_categories = ["en:other"]

        return off_categories

    def get_off_categories_of_fdc_product(self, given_category: str) -> list[str]:
        off_categories = []

        given_off_categories = self.fdc_to_off_categories.get(given_category)

        if given_off_categories is not None:
            for searched_category in given_off_categories:
                for key, value in self.off_categories.items():
                    off_cat_list = value["values"]
                    if searched_category in off_cat_list:
                        off_categories.append(key)
                        break

        if not off_categories:
            cat = re.sub(" +[-&/()]* *|[=&/()]", "-", given_category.strip())
            off_categories = ["en:" + cat.rstrip("-").lower().replace(",", "") + "-fdc"]

        return off_categories

    def __get_off_categories_from_given_categories(
        self, given_categories_list: list[str]
    ) -> list[str]:
        off_categories = []

        if given_categories_list is not None:
            for given_category in given_categories_list:
                for key, value in self.off_categories.items():
                    categories_list = value["values"]

                    if given_category in categories_list:
                        for found_cat in off_categories:
                            if key in self.off_categories[found_cat]["parents"]:
                                return off_categories

                        off_categories.append(key)

        return off_categories
