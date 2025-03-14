from domain.mapper.brands_mapper import BrandsMapper
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.food_groups_mapper import FoodGroupsMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nova_data_mapper import NovaDataMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.product.product import Product
from domain.utils.converter import Converter
from domain.validator.nova_data_validator import NovaDataValidator
from domain.validator.product_validator import ProductValidator
from datetime import datetime, timezone


class ProductMapper:
    WANTED_COUNTRIES = ["Canada", "United States", "New Zealand"]

    def __init__(
        self,
        ingredients_mapper: IngredientsMapper,
        nutriscore_data_mapper: NutriscoreDataMapper,
    ):
        self.ingredients_mapper = ingredients_mapper
        self.nutriscore_data_mapper = nutriscore_data_mapper

    def map_fdc_dict_to_product(self, product_dict: dict) -> Product:
        """Maps a fdc dictionary to a product object"""
        id_field = "gtinUpc"
        product_name_field = "description"
        generic_name_field = "description"
        data_source_field = "dataSource"
        modified_date_field = "modifiedDate"
        available_date_field = "availableDate"
        publication_date_field = "publicationDate"
        brands_field = "brandName"
        brand_owner_field = "brandOwner"

        food_groups_en_field = (
            "brandedFoodCategory"  # TODO convert fdc categories to off food groups
        )

        return Product(
            id_match=product_dict[id_field].lstrip("0"),
            id_original=product_dict[id_field],
            product_name=product_dict[product_name_field].title(),
            generic_name_en=product_dict[generic_name_field].title(),
            data_source=product_dict[data_source_field],
            modified_date=datetime.strptime(
                product_dict[modified_date_field], "%m/%d/%Y"
            ),
            available_date=datetime.strptime(
                product_dict[available_date_field], "%m/%d/%Y"
            ),
            publication_date=datetime.strptime(
                product_dict[publication_date_field], "%m/%d/%Y"
            ),
            quantity=product_dict["householdServingFullText"],
            is_raw=self.fdc_is_raw_aliment(product_dict["brandedFoodCategory"]),
            brands=(
                [product_dict[brands_field].title()]
                if brands_field in product_dict.keys()
                else []
            ),
            brand_owner=product_dict[brand_owner_field].title(),
            food_groups_en=product_dict[food_groups_en_field].split(","),
            ingredients=self.ingredients_mapper.map_fdc_dict_to_ingredients(
                product_dict["ingredients"]
            ),
            serving_size=product_dict["servingSize"],
            serving_size_unit=product_dict["servingSizeUnit"],
            nutrition_facts=NutritionFactsMapper.map_fdc_dict_to_nutrition_facts(
                product_dict["foodNutrients"]
            ),
            nutriscore_data=self.nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(
                product_dict["foodNutrients"]
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
        quantity_name_index = header.index("quantity")
        serving_size_index = header.index("serving_quantity")
        modified_date_index = header.index("last_modified_t")

        return Product(
            id_match=row[id_index].lstrip("0"),
            id_original=row[id_index],
            product_name=(
                row[product_name_index].strip()
                if row[product_name_index] is not None
                else None
            ),
            generic_name_en=(
                row[generic_name_index].strip()
                if row[generic_name_index] is not None
                else None
            ),
            modified_date=datetime.fromtimestamp(Converter.safe_int(row[modified_date_index]), tz=timezone.utc),
            quantity=row[quantity_name_index],
            is_raw=self.off_csv_is_raw_aliment(row, header),
            brands=BrandsMapper.map_off_row_to_brands(row, header),
            brand_owner=BrandsMapper.map_off_row_to_brand_owner(row, header),
            food_groups_en=FoodGroupsMapper.map_off_row_to_food_groups(row, header),
            ingredients=self.ingredients_mapper.map_off_row_to_ingredients(row, header),
            serving_size=Converter.safe_float(row[serving_size_index]),
            nutrition_facts=NutritionFactsMapper.map_off_row_to_nutrition_facts(
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
            country in product_dict.get(country_field, [])
            for country in ProductMapper.WANTED_COUNTRIES
        ):
            return None

        id_field = "code"
        product_name_field = "product_name"
        generic_name_field = "generic_name"
        modified_date_field = "last_modified_t"
        brands_field = "brands"
        brand_owner_field = "brand_owner"
        food_groups_en_field = "food_groups"
        quantity_name_field = "quantity"
        serving_size_field = "serving_quantity"
        serving_size_unit_field = "serving_quantity_unit"

        return Product(
            id_match=product_dict.get(id_field).lstrip("0"),
            id_original=product_dict.get(id_field),
            product_name=(
                product_dict.get(product_name_field).strip()
                if product_dict.get(product_name_field) is not None
                else None
            ),
            generic_name_en=(
                product_dict.get(generic_name_field).strip()
                if product_dict.get(generic_name_field) is not None
                else None
            ),
            modified_date=datetime.fromtimestamp(product_dict.get(modified_date_field), tz=timezone.utc),
            quantity=product_dict.get(quantity_name_field),
            is_raw=self.off_json_is_raw_aliment(product_dict),
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
            serving_size=product_dict.get(serving_size_field),
            serving_size_unit=product_dict.get(serving_size_unit_field),
            nutrition_facts=NutritionFactsMapper.map_off_dict_to_nutrition_facts(
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
    def off_csv_is_raw_aliment(row: list[str], header: list[str]):
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
    def off_json_is_raw_aliment(product_dict: dict) -> bool:
        """Checks if the aliment is raw based on its dict values"""
        # Check the NOVA group
        nova_field = "nova_group"
        nova_group = product_dict.get(nova_field)

        try:
            if NovaDataValidator.check_nova_raw_group(nova_group):
                return True
            if NovaDataValidator.check_nova_transformed_group(nova_group):
                return False
        except ValueError:
            pass

        # Check the PNNS groups
        pnns_field = "pnns_groups_1"
        if ProductValidator.check_pnns_groups(product_dict.get(pnns_field)):
            return True

        # Check the categories
        cat_field = "categories_tags"
        if ProductValidator.check_list_categories(product_dict.get(cat_field)):
            return True

        # Check the additives
        additives_field = "additives_n"
        try:
            if ProductValidator.check_additives(
                product_dict.get(additives_field), nova_group
            ):
                return True
        except ValueError:
            pass

        return False

    @staticmethod
    def fdc_is_raw_aliment(category: str):
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
