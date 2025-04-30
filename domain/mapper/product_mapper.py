from domain.mapper.brands_mapper import BrandsMapper
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.food_groups_mapper import FoodGroupsMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nova_data_mapper import NovaDataMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.category_mapper import CategoryMapper
from domain.product.product import Product
from domain.utils.converter import Converter
from domain.validator.nova_data_validator import NovaDataValidator
from domain.validator.product_validator import ProductValidator
from datetime import datetime, timezone


class ProductMapper:
    """
    This is a class that maps objects (rows or dicts) read from different files to Product objects.

    Methods:
        map_fdc_dict_to_product(product_dict): Maps the given dictionary to a Product object
        map_off_row_to_product(row, header): Maps the given csv row to a Product object
        map_off_dict_to_product(product_dict): Maps the given dictionary to a Product object
    """

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
        """Maps a dictionary from an FDC json export to a product object"""
        id_field = "gtinUpc"
        fdc_id_field = "fdcId"
        product_name_field = "description"
        data_source_field = "dataSource"
        modified_date_field = "modifiedDate"
        available_date_field = "availableDate"
        publication_date_field = "publicationDate"
        brands_field = "brandName"
        brand_owner_field = "brandOwner"
        ingredients_field = "ingredients"
        food_nutrients_field = "foodNutrients"

        category_field = (
            "brandedFoodCategory"  # TODO convert fdc categories to off food groups
        )

        return Product(
            id_match=product_dict[id_field]
            .strip()
            .replace(" ", "")
            .replace("-", "")
            .lstrip("0"),
            id_original=product_dict[id_field].strip(),
            fdc_id=str(product_dict[fdc_id_field]).strip(),
            product_name=product_dict[product_name_field].strip().title(),
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
            quantity=product_dict.get("packageWeight"),
            household_serving_fulltext=product_dict["householdServingFullText"],
            is_raw=self.__fdc_is_raw_aliment(product_dict[category_field]),
            brands=(
                [product_dict[brands_field].strip()]
                if brands_field in product_dict.keys()
                else []
            ),
            brand_owner=(
                None
                if product_dict[brand_owner_field].strip().upper()
                == "NOT A BRANDED ITEM"
                else product_dict[brand_owner_field].strip()
            ),
            off_categories_en=self.category_mapper.get_off_categories_of_fdc_product(
                product_dict.get(category_field)
            ),
            fdc_category_en=product_dict.get(category_field),
            food_groups_en=list(
                filter(None, map(str.strip, product_dict[category_field].split(",")))
            ),  # TODO compléter la liste si possible
            ingredients=self.ingredients_mapper.map_fdc_dict_to_ingredients(
                product_dict[ingredients_field]
            ),
            serving_size=product_dict["servingSize"],
            serving_size_unit=product_dict["servingSizeUnit"],
            nutrition_facts=self.nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
                product_dict[food_nutrients_field],
                product_dict.get("labelNutrients"),
                product_dict.get("preparationStateCode"),
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
        """Maps a row from a csv export of OFF to a product object"""

        id_index = header.index("code")
        product_name_index = header.index("product_name")
        quantity_name_index = header.index("quantity")
        serving_size_index = header.index("serving_quantity")
        modified_date_index = header.index("last_modified_t")
        category_tag_index = header.index("categories_tags")

        return Product(
            id_match=row[id_index].strip().lstrip("0").replace("-", ""),
            id_original=row[id_index].strip(),
            product_name=(
                row[product_name_index].strip().title()
                if row[product_name_index] != ""
                else None
            ),
            modified_date=datetime.fromtimestamp(
                Converter.safe_int(row[modified_date_index]), tz=timezone.utc
            ),
            quantity=row[quantity_name_index],
            is_raw=self.__off_csv_is_raw_aliment(row, header),
            brands=BrandsMapper.map_off_row_to_brands(row, header),
            brand_owner=BrandsMapper.map_off_row_to_brand_owner(row, header),
            off_categories_en=self.category_mapper.get_off_categories_of_off_product(
                row[category_tag_index]
            ),
            food_groups_en=FoodGroupsMapper.map_off_row_to_food_groups(row, header),
            ingredients=self.ingredients_mapper.map_off_row_to_ingredients(row, header),
            serving_size=Converter.safe_float(row[serving_size_index]),
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
        """Maps a dictionary from a jsonl export of OFF to a product object"""

        id_field = "code"
        product_name_field = "product_name"
        modified_date_field = "last_modified_t"
        category_field = "categories"
        brands_field = "brands"
        brand_owner_field = "brand_owner"
        food_groups_en_field = "food_groups"
        quantity_name_field = "quantity"
        serving_size_field = "serving_quantity"
        serving_size_unit_field = "serving_quantity_unit"
        nutrition_data_per_field = "nutrition_data_per"

        modified_timestamp = product_dict.get(modified_date_field)
        modified_date = (
            datetime.fromtimestamp(modified_timestamp, tz=timezone.utc)
            if modified_timestamp is not None
            else None
        )

        return Product(
            id_match=product_dict.get(id_field).strip().lstrip("0").replace("-", ""),
            id_original=product_dict.get(id_field).strip(),
            product_name=product_dict.get(product_name_field, "").strip().title()
            or None,
            modified_date=modified_date,
            quantity=product_dict.get(quantity_name_field),
            off_categories_en=product_dict.get(category_field),
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
            serving_size=product_dict.get(serving_size_field),
            serving_size_unit=product_dict.get(serving_size_unit_field),
            nutrition_data_per=product_dict.get(nutrition_data_per_field),
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
    def __off_csv_is_raw_aliment(row: list[str], header: list[str]) -> bool:
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
    def __fdc_is_raw_aliment(category: str) -> bool:
        """Checks if the aliment is raw based on its category"""
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
