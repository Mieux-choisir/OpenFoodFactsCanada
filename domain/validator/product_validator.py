class ProductValidator:
    """
    This is a class that validates data related to the products.

    Methods:
      check_pnns_groups(pnns): Checks if the given pnns group string is either cereals or legumes
      check_string_categories(category): Checks if the given category is a foundation food AND not a non foundation food
      check_list_categories(category): Checks if the given category is a foundation food AND not a non foundation food
      check_additives(additives, nova_group): Checks if there are no additives and the nova group is less than or equal to 2
    """

    raw_food_categories = {
        "en:flours": True,
        "en:rices": True,
        "en:pastas": True,
        "en:breads": True,
        "en:legumes": True,
        "en:eggs": True,
        "en:milks": True,
        "en:plain-yogurts": True,
        "en:vegetables": True,
        "en:fruits": True,
        "en:nuts": True,
        "en:seeds": True,
    }

    transformed_food_categories = {
        "en:snacks": True,
        "en:beverages": True,
        "en:desserts": True,
        "en:candies": True,
        "en:chocolates": True,
        "en:breakfast-cereals": True,
        "en:processed-meats": True,
    }

    @staticmethod
    def check_pnns_groups(pnns: str) -> bool:
        """Returns True if the given pnns group is either cereals or legumes, False otherwise"""
        if pnns in ["cereals", "legumes"]:
            return True
        return False

    @staticmethod
    def check_string_categories(category: str) -> bool:
        """Returns True if the given category is a foundation food AND not a non foundation food, False otherwise"""
        if category:
            categories = set(category.split(","))
            if any(cat in ProductValidator.raw_food_categories for cat in categories):
                if not any(
                    cat in ProductValidator.transformed_food_categories
                    for cat in categories
                ):
                    return True
        return False

    @staticmethod
    def check_list_categories(category: list) -> bool:
        """Returns True if the given category is a foundation food AND not a non foundation food, False otherwise"""
        if (
            category
            and any(cat in ProductValidator.raw_food_categories for cat in category)
            and not any(
                cat in ProductValidator.transformed_food_categories for cat in category
            )
        ):
            return True
        return False

    @staticmethod
    def check_additives(additives: str, nova_group: str) -> bool:
        """Returns True if there are no additives and the nova group is less than or equal to 2, False otherwise"""
        if additives and additives != "":
            try:
                if (
                    int(additives) == 0
                    and nova_group
                    and nova_group != ""
                    and int(nova_group) <= 2
                ):
                    return True
            except ValueError:
                raise ValueError
        return False
