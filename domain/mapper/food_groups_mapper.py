class FoodGroupsMapper:

    @staticmethod
    def map_off_row_to_food_groups(row: list[str], header: list[str]) -> list[str]:
        food_groups_index = header.index("food_groups_en")

        food_groups = []
        if row[food_groups_index] != "":
            food_groups = list(
                filter(None, map(str.strip, row[food_groups_index].lower().split(",")))
            )
        return food_groups

    @staticmethod
    def map_off_dict_to_food_groups(
        product_dict: dict, food_groups_en_field: str
    ) -> list[str]:
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
