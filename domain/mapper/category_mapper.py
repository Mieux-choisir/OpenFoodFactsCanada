import re

from domain.utils.category_creator import CategoryCreator


class CategoryMapper:
    """
    This is a class that maps products values to Open Food Facts categories.

    Attributes:
        off_categories (dict): A dictionary where the keys are the canonical terms of categories and the values are dictionaries with the fields:
            - values: all the possible terms for the category
            - parents: all the immediate parents of the category
        fdc_to_off_categories (dict): A dictionary where the keys are the fdc categories and the values are the list of their corresponding Open
        Food Facts categories

    Methods:
        get_off_categories_of_off_product(given_categories): Maps the given categories string of a OFF product to a categories list
        get_off_categories_of_fdc_product(given_category): Maps the given category string of an FDC product to a categories list
    """

    def __init__(
        self,
        category_creator: CategoryCreator,
        off_taxonomy_file: str,
        fdc_off_mapping_file: str,
    ):
        self.off_categories: dict = category_creator.create_off_categories(
            off_taxonomy_file
        )
        self.fdc_to_off_categories: dict = (
            category_creator.create_fdc_to_off_categories_mapping(
                fdc_off_mapping_file, self.off_categories
            )
        )

    def get_off_categories_of_off_product(self, given_categories: str) -> list[str]:
        """Maps the values in a given OFF product to a list of its OFF categories"""
        if not given_categories:
            return ["en:other"]

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
        """Maps the values in a given FDC product to a list of its OFF categories"""
        off_categories = []

        given_off_categories = self.fdc_to_off_categories.get(given_category)

        if given_off_categories is not None:
            for searched_category in given_off_categories:
                for key, value in self.off_categories.items():
                    off_cat_list = value["values"]
                    if searched_category in off_cat_list:
                        off_categories.append(key)
                        break

        return off_categories

    @staticmethod
    def get_fdc_category(category: str) -> str:
        """Returns the formatted given FDC category"""
        formatted_category = re.sub(
            " +[-&/()']* *|[=&/()]", "-", category.strip().lower().replace(",", "")
        )
        formatted_category = "en:" + formatted_category.rstrip("-")

        return formatted_category

    def __get_off_categories_from_given_categories(
        self, given_categories_list: list[str]
    ) -> list[str]:
        """Returns a list of the most specific categories existing in the off_categories dict from the given categories list"""
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
