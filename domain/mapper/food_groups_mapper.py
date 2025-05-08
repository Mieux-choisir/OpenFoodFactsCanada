class FoodGroupsMapper:
    """
    This is a class that maps products values to lists of food groups (list[str]).

    Methods:
        map_off_dict_to_food_groups(product_dict): Maps the given dictionary to a list of food groups
    """

    @staticmethod
    def map_off_dict_to_food_groups(
        product_dict: dict, food_groups_en_field: str
    ) -> list[str]:
        """Maps the values in a given OFF (jsonl) product to a list of food groups (str)"""
        food_groups = []

        if (
            food_groups_en_field in product_dict
            and product_dict[food_groups_en_field] is not None
        ):
            food_groups = list(
                filter(
                    None,
                    map(
                        str.strip, product_dict[food_groups_en_field].lower().split(",")
                    ),
                )
            )
        return food_groups
