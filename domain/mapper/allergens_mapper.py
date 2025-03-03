class AllergensMapper:

    @staticmethod
    def map_off_row_to_allergens(row: list[str], header: list[str]) -> list[str]:
        allergens_index = header.index("allergens")

        allergens = []
        if row[allergens_index] != "" and row[allergens_index] is not None:
            allergens = row[allergens_index].split(",")
        return allergens

    @staticmethod
    def map_off_dict_to_allergens(product_dict: dict, allergens_en_field: str) -> list[str]:
        allergens_value = []
        if product_dict[allergens_en_field] != "":
            allergens_value = product_dict[allergens_en_field].split(",")
        return allergens_value
