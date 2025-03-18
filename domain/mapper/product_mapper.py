from domain.mapper.brands_mapper import BrandsMapper
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.food_groups_mapper import FoodGroupsMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nova_data_mapper import NovaDataMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.category_mapper import CategoryMapper
from domain.product.product import Product
from domain.validator.nova_data_validator import NovaDataValidator
from domain.validator.product_validator import ProductValidator


class ProductMapper:
    WANTED_COUNTRIES = ["Canada", "United States"]

    def __init__(
        self,
        ingredients_mapper: IngredientsMapper,
        nutriscore_data_mapper: NutriscoreDataMapper,
        nutrition_facts_mapper: NutritionFactsMapper,
        category_mapper: CategoryMapper,
    ):
        self.ingredients_mapper = ingredients_mapper
        self.nutriscore_data_mapper = nutriscore_data_mapper
        self.nutrition_facts_mapper = nutrition_facts_mapper
        self.category_mapper = category_mapper

    def map_fdc_dict_to_product(self, product_dict: dict) -> Product:
        """Maps a fdc dictionary to a product object"""
        id_field = "gtinUpc"
        product_name_field = "description"
        generic_name_field = "description"
        brands_field = "brandName"
        brand_owner_field = "brandOwner"
        ingredients_field = "ingredients"
        food_nutrients_field = "foodNutrients"

        category_field = (
            "brandedFoodCategory"  # TODO convert fdc categories to off food groups
        )

        return Product(
            id_match=product_dict[id_field].strip().lstrip("0"),
            id_original=product_dict[id_field].strip(),
            product_name=product_dict[product_name_field].strip().title(),
            generic_name_en=product_dict[generic_name_field].strip().title(),
            is_raw=self.__fdc_is_raw_aliment(product_dict[category_field]),
            brands=(
                [product_dict[brands_field].strip().title()]
                if brands_field in product_dict.keys()
                else []
            ),
            brand_owner=product_dict[brand_owner_field].strip().title(),
            categories_en=self.category_mapper.get_off_categories_of_fdc_product(
                product_dict.get(category_field)
            ),
            food_groups_en=list(
                filter(None, map(str.strip, product_dict[category_field].split(",")))
            ),  # TODO compléter la liste si possible
            ingredients=self.ingredients_mapper.map_fdc_dict_to_ingredients(
                product_dict[ingredients_field]
            ),
            nutrition_facts=self.nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
                product_dict[food_nutrients_field]
            ),
            nutriscore_data=self.nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(
                product_dict[food_nutrients_field]
            ),
            ecoscore_data=None,
            nova_data=None,
        )

    def map_off_row_to_product(
        self, row: list[str], header: list[str]
    ) -> Product | None:
        country_index = header.index("countries_en")
        if not any(
            country in row[country_index] for country in ProductMapper.WANTED_COUNTRIES
        ):
            return None

        id_index = header.index("code")
        product_name_index = header.index("product_name")
        generic_name_index = header.index("generic_name")
        category_tag_index = header.index("categories_tags")

        return Product(
            id_match=row[id_index].strip().lstrip("0"),
            id_original=row[id_index].strip(),
            product_name=(
                row[product_name_index].strip().title()
                if row[product_name_index] != ""
                else None
            ),
            generic_name_en=(
                row[generic_name_index].strip().title()
                if row[generic_name_index] != ""
                else None
            ),
            is_raw=self.__off_csv_is_raw_aliment(row, header),
            brands=BrandsMapper.map_off_row_to_brands(row, header),
            brand_owner=BrandsMapper.map_off_row_to_brand_owner(row, header),
            categories_en=self.category_mapper.get_off_categories_of_off_product(
                row[category_tag_index]
            ),
            food_groups_en=FoodGroupsMapper.map_off_row_to_food_groups(row, header),
            ingredients=self.ingredients_mapper.map_off_row_to_ingredients(row, header),
            nutrition_facts=self.nutrition_facts_mapper.map_off_row_to_nutrition_facts(
                row, header
            ),
            nutriscore_data=self.nutriscore_data_mapper.map_off_row_to_nutriscore_data(
                row, header
            ),
            ecoscore_data=EcoscoreDataMapper.map_off_row_to_ecoscore_data(row, header),
            nova_data=NovaDataMapper.map_off_row_to_nova_data(row, header),
        )

    def map_off_dict_to_product(self, product_dict: dict) -> Product | None:
        country_field = "countries"
        if not any(
            country in product_dict[country_field]
            for country in ProductMapper.WANTED_COUNTRIES
        ):
            return None

        id_field = "code"
        product_name_field = "product_name"
        generic_name_field = "generic_name"
        category_field = "categories"
        brands_field = "brands"
        brand_owner_field = "brand_owner"
        food_groups_en_field = "food_groups"

        return Product(
            id_match=product_dict[id_field].strip().lstrip("0"),
            id_original=product_dict[id_field].strip(),
            product_name=(
                product_dict[product_name_field].strip().title()
                if product_dict[product_name_field].strip() != ""
                else None
            ),
            generic_name_en=(
                product_dict[generic_name_field].strip().title()
                if product_dict[generic_name_field] is not None
                and product_dict[generic_name_field].strip() != ""
                else None
            ),
            categories_en=self.category_mapper.get_off_categories_of_off_product(
                product_dict[category_field]
            ),
            is_raw=self.__off_json_is_raw_aliment(product_dict),
            brands=BrandsMapper.map_off_dict_to_brands(product_dict, brands_field),
            brand_owner=BrandsMapper.map_off_dict_to_brand_owner(
                product_dict, brand_owner_field, brands_field
            ),
            food_groups_en=FoodGroupsMapper.map_off_dict_to_food_groups(
                product_dict, food_groups_en_field
            ),
            ingredients=self.ingredients_mapper.map_off_dict_to_ingredients(
                product_dict
            ),
            nutrition_facts=self.nutrition_facts_mapper.map_off_dict_to_nutrition_facts(
                product_dict
            ),
            nutriscore_data=self.nutriscore_data_mapper.map_off_dict_to_nutriscore_data(
                product_dict
            ),
            ecoscore_data=EcoscoreDataMapper.map_off_dict_to_ecoscore_data(
                product_dict
            ),
            nova_data=NovaDataMapper.map_off_dict_to_nova_data(product_dict),
        )

    @staticmethod
    def __off_csv_is_raw_aliment(row: list[str], header: list[str]):
        """Checks if the aliment is raw based on its row values"""
        # Check the NOVA group
        nova_index = header.index("nova_group")
        nova_group = row[nova_index]
        try:
            if NovaDataValidator.check_nova_raw_group(nova_group):
                return True
            if NovaDataValidator.check_nova_transformed_group(nova_group):
                return False
        except ValueError:
            pass

        # Check the PNNS groups
        pnns_index = header.index("pnns_groups_1")
        if ProductValidator.check_pnns_groups(row[pnns_index]):
            return True

        # Check the categories
        cat_index = header.index("categories_tags")
        if ProductValidator.check_string_categories(row[cat_index]):
            return True

        # Check the additives
        additives_index = header.index("additives_n")
        try:
            if ProductValidator.check_additives(row[additives_index], nova_group):
                return True
        except ValueError:
            pass

        return False

    @staticmethod
    def __off_json_is_raw_aliment(product_dict: dict) -> bool:
        """Checks if the aliment is raw based on its dict values"""
        # Check the NOVA group
        nova_field = "nova_group"
        nova_group = product_dict[nova_field]

        try:
            if NovaDataValidator.check_nova_raw_group(nova_group):
                return True
            if NovaDataValidator.check_nova_transformed_group(nova_group):
                return False
        except ValueError:
            pass

        # Check the PNNS groups
        pnns_field = "pnns_groups_1"
        if ProductValidator.check_pnns_groups(product_dict[pnns_field]):
            return True

        # Check the categories
        cat_field = "categories_tags"
        if ProductValidator.check_list_categories(product_dict[cat_field]):
            return True

        # Check the additives
        additives_field = "additives_n"
        try:
            if ProductValidator.check_additives(
                product_dict[additives_field], nova_group
            ):
                return True
        except ValueError:
            pass

        return False

    @staticmethod
    def __fdc_is_raw_aliment(category: str):
        is_raw = False

        if category in [
            "Vegetables  Unprepared/Unprocessed (Frozen)",
            "Fruits, Vegetables & Produce",
            "Vegetables - Unprepared/Unprocessed (Frozen)",
        ]:
            is_raw = True
        elif category == "Pre-Packaged Fruit & Vegetables":
            is_raw = None  # currently no way of knowing if the product is raw, there should be a more complex analysis
        return is_raw
