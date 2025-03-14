class FoodGroupsMapper:

    @staticmethod
    def map_off_row_to_food_groups(row: list[str], header: list[str]) -> list[str]:
        food_groups_index = header.index("food_groups_en")

        food_groups = []
        if row[food_groups_index] is not None:
            food_groups = row[food_groups_index].split(",")
        return food_groups

    @staticmethod
    def map_off_dict_to_food_groups(
        product_dict: dict, food_groups_en_field: str
    ) -> list[str]:
        food_groups = []
        if product_dict.get(food_groups_en_field) is not None:
            food_groups = product_dict.get(food_groups_en_field).split(",")
        return food_groups
