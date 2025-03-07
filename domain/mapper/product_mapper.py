from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nova_data_mapper import NovaDataMapper
from domain.mapper.number_mapper import NumberMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.product.product import Product
from domain.validator.nova_data_validator import NovaDataValidator
from domain.validator.product_validator import ProductValidator


class ProductMapper:
    WANTED_COUNTRY = "Canada"

    def __init__(self, ingredients_mapper: IngredientsMapper):
        self.ingredients_mapper = ingredients_mapper

    def map_fdc_dict_to_product(self, dict: dict) -> Product:
        """Maps a fdc dictionary to a product object"""
        id_field = "gtinUpc"
        product_name_field = "description"
        generic_name_field = "description"
        brand_owner_field = "brandOwner"
        ingredients_field = "ingredients"
        food_nutrients_field = "foodNutrients"

        return Product(
            id=dict[id_field].strip(),
            product_name=dict[product_name_field].strip().title(),
            generic_name_en=dict[generic_name_field].strip().title(),
            is_raw=None,  # TODO verifier si cest toujours cru ou pas
            brand_name=dict[brand_owner_field].strip().title(),
            food_groups_en=[],  # TODO compléter la liste si possible
            ingredients=self.ingredients_mapper.map_fdc_dict_to_ingredients(
                dict[ingredients_field]
            ),
            nutrition_facts=NutritionFactsMapper.map_fdc_dict_to_nutrition_facts(
                dict[food_nutrients_field]
            ),
            allergens=[],  # TODO compléter la liste si possible
            nutriscore_data=NutriscoreDataMapper.map_fdc_dict_to_nutriscore_data(
                dict[food_nutrients_field]
            ),
            ecoscore_data=None,
            nova_data=None,
        )

    def map_off_row_to_product(
        self, row: list[str], header: list[str]
    ) -> Product | None:
        country_field = header.index("countries_en")
        if ProductMapper.WANTED_COUNTRY not in row[country_field]:
            return None

        id_field = header.index("code")
        product_name_field = header.index("product_name")
        generic_name_field = header.index("generic_name")
        brand_owner_field = header.index("brands")
        food_groups_en_field = header.index("food_groups_en")
        allergens_en_field = header.index("allergens_en")

        nutriscore_data_mapper = NutriscoreDataMapper(NumberMapper())

        return Product(
            id=row[id_field].strip(),
            product_name=row[product_name_field].strip().title(),
            generic_name_en=row[generic_name_field].strip().title(),
            is_raw=self.__off_csv_is_raw_aliment(row, header),
            brand_name=row[brand_owner_field].strip().title(),
            food_groups_en=list(filter(None, map(str.strip, row[food_groups_en_field].split(",")))),
            ingredients=self.ingredients_mapper.map_off_row_to_ingredients(row, header),
            nutrition_facts=NutritionFactsMapper.map_off_row_to_nutrition_facts(
                row, header
            ),
            allergens=list(filter(None, map(str.strip, row[allergens_en_field].split(",")))),
            nutriscore_data=nutriscore_data_mapper.map_off_row_to_nutriscore_data(
                row, header
            ),
            ecoscore_data=EcoscoreDataMapper.map_off_row_to_ecoscore_data(row, header),
            nova_data=NovaDataMapper.map_off_row_to_nova_data(row, header),
        )

    def map_off_dict_to_product(self, product_dict: dict) -> Product | None:
        country_field = "countries"
        if ProductMapper.WANTED_COUNTRY not in product_dict[country_field]:
            return None

        id_field = "code"
        product_name_field = "product_name"
        generic_name_field = "generic_name"
        brand_owner_field = "brands"
        food_groups_en_field = "food_groups"
        allergens_en_field = "allergens"

        return Product(
            id=product_dict[id_field].strip(),
            product_name=product_dict[product_name_field].strip().title(),
            generic_name_en=product_dict[generic_name_field].strip().title(),
            is_raw=self.__off_json_is_raw_aliment(product_dict),
            brand_name=product_dict[brand_owner_field].strip().title(),
            food_groups_en=list(filter(None, map(str.strip, product_dict[food_groups_en_field].split(",")))),
            ingredients=self.ingredients_mapper.map_off_dict_to_ingredients(
                product_dict
            ),
            nutrition_facts=NutritionFactsMapper.map_off_dict_to_nutrition_facts(
                product_dict
            ),
            allergens=list(filter(None, map(str.strip, product_dict[allergens_en_field].split(",")))),
            nutriscore_data=NutriscoreDataMapper.map_off_dict_to_nutriscore_data(
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
        nova_idx = header.index("nova_group")
        nova_group = row[nova_idx]
        try:
            if NovaDataValidator.check_nova_raw_group(nova_group):
                return True
            if NovaDataValidator.check_nova_transformed_group(nova_group):
                return False
        except ValueError:
            pass

        # Check the PNNS groups
        pnns_idx = header.index("pnns_groups_1")
        if ProductValidator.check_pnn_groups(row[pnns_idx]):
            return True

        # Check the categories
        cat_idx = header.index("categories_tags")
        if ProductValidator.check_string_categories(row[cat_idx]):
            return True

        # Check the additives
        additives_idx = header.index("additives_n")
        try:
            if ProductValidator.check_additives(row[additives_idx], nova_group):
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
        if ProductValidator.check_pnn_groups(product_dict[pnns_field]):
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
