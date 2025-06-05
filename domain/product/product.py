# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import datetime
import logging
from typing import Optional, List, Dict, Any

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrition_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData


class Product(ComplexField):
    """
    This is a class that stores data on the Nova data of a product.

    Attributes:
        id_match (Optional[int]): The formatted id used to match the products
        id_original (dict): The original id (not formatted) of the product
        product_name (Optional[str]): The name of the product
        data_source (Optional[str]): The source of the data obtained from the product
        modified_date (Optional[datetime.datetime]): The last date data of the product was modified
        available_date (Optional[datetime.datetime]): The date data of the product became first available
        publication_date (Optional[datetime.datetime]): The date data of the product was published
        quantity (Optional[str]): Quantity of the product
        categories_en (list[str]): List of the different categories of the product
        is_raw (Optional[bool]): Boolean indicating if the product is a raw product
        brands (list[str]): List of the brands of the product
        brand_owner (Optional[str]): Brand owner of the product
        food_groups_en (list[str]): List of the food groups of the product
        ingredients (Optional[Ingredients]): Data about the ingredients of the product
        serving_size (Optional[float]): The serving size of the product
        serving_size_unit (Optional[str]): The unit of the serving size of the product
        nutrition_facts (Optional[NutritionFacts]): Data about the nutrition facts of the product
        nutriscore_data (Optional[NutriscoreData]): Data about the NutriScore of the product
        ecoscore_data (Optional[EcoscoreData]): Data about the Eco-score of the product
        nova_data (Optional[NovaData]): Data about the Nova group of the product

    Methods:
        has_at_least_one_score(): Indicates whether the product has at least one score available (NutriScore, Eco-score or Nova group)
    """

    id_match: Optional[str] = None
    id_original: Optional[str] = None
    fdc_id: Optional[str] = None
    product_name: Optional[str] = None
    data_source: Optional[str] = None
    modified_date: Optional[datetime.datetime] = None
    available_date: Optional[datetime.datetime] = None
    publication_date: Optional[datetime.datetime] = None
    household_serving_fulltext: Optional[str] = None
    quantity: Optional[str] = None
    off_categories_en: list[str] = []
    fdc_category_en: Optional[str] = None
    is_raw: Optional[bool] = None
    brands: List[str] = []
    brand_owner: Optional[str] = None
    food_groups_en: List[str] = []
    ingredients: Optional[Ingredients] = None
    serving_size: Optional[float] = None
    serving_size_unit: Optional[str] = None
    nutrition_data_per: Optional[str] = None
    nutrition_facts: Optional[NutritionFacts] = None
    nutriscore_data: Optional[NutriscoreData] = NutriscoreData()
    ecoscore_data: Optional[EcoscoreData] = EcoscoreData()
    nova_data: Optional[NovaData] = NovaData()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Creates a Product object from a data dictionary"""

        def parse_mongo_date(date_value):
            if not date_value:
                return None
            if isinstance(date_value, str):
                try:
                    return cls.parse_date(date_value)
                except Exception as e:
                    logging.warning(f"Cannot parse the date '{date_value}': {e}")
                    return None
            return date_value

        id_match = data.get("id_match")
        id_original = data.get("id_original")
        fdc_id = data.get("fdc_id")
        product_name = data.get("product_name")
        data_source = data.get("data_source")

        modified_date = parse_mongo_date(data.get("modified_date"))
        available_date = parse_mongo_date(data.get("available_date"))
        publication_date = parse_mongo_date(data.get("publication_date"))

        household_serving_fulltext = data.get("household_serving_fulltext")
        quantity = data.get("quantity")
        off_categories_en = data.get("off_categories_en", [])
        fdc_category_en = data.get("fdc_category_en")
        is_raw = data.get("is_raw")
        brands = data.get("brands", [])
        brand_owner = data.get("brand_owner")
        food_groups_en = data.get("food_groups_en", [])
        serving_size = data.get("serving_size")
        serving_size_unit = data.get("serving_size_unit")
        nutrition_data_per = data.get("nutrition_data_per")

        ingredients_data = data.get("ingredients")
        ingredients = (
            Ingredients.from_dict(ingredients_data)
            if ingredients_data is not None
            else None
        )

        nutrition_data = data.get("nutrition_facts")
        nutrition_facts = (
            NutritionFacts.from_dict(nutrition_data)
            if nutrition_data is not None
            else None
        )

        nutriscore_data_dict = data.get("nutriscore_data")
        nutriscore_data = (
            NutriscoreData.from_dict(nutriscore_data_dict)
            if nutriscore_data_dict is not None
            else NutriscoreData()
        )

        ecoscore_data_dict = data.get("ecoscore_data")
        ecoscore_data = (
            EcoscoreData.from_dict(ecoscore_data_dict)
            if ecoscore_data_dict is not None
            else EcoscoreData()
        )

        nova_data_dict = data.get("nova_data")
        nova_data = (
            NovaData.from_dict(nova_data_dict)
            if nova_data_dict is not None
            else NovaData()
        )

        return cls(
            id_match=id_match,
            id_original=id_original,
            fdc_id=fdc_id,
            product_name=product_name,
            data_source=data_source,
            modified_date=modified_date,
            available_date=available_date,
            publication_date=publication_date,
            household_serving_fulltext=household_serving_fulltext,
            quantity=quantity,
            off_categories_en=off_categories_en,
            fdc_category_en=fdc_category_en,
            is_raw=is_raw,
            brands=brands,
            brand_owner=brand_owner,
            food_groups_en=food_groups_en,
            ingredients=ingredients,
            serving_size=serving_size,
            serving_size_unit=serving_size_unit,
            nutrition_data_per=nutrition_data_per,
            nutrition_facts=nutrition_facts,
            nutriscore_data=nutriscore_data,
            ecoscore_data=ecoscore_data,
            nova_data=nova_data,
        )

    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime.datetime]:
        if date_str:
            try:
                return datetime.datetime.fromisoformat(date_str)
            except ValueError:
                return None
        return None
