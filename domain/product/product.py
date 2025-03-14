# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import datetime
from typing import Optional, List

from domain.product.category_enum import CategoryEnum
from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData


class Product(ComplexField):
    id_match: Optional[str] = None
    id_original: Optional[str] = None
    generic_name_en: Optional[str] = None
    product_name: Optional[str] = None
    data_source: Optional[str] = None
    modified_date: Optional[datetime.datetime] = None
    available_date: Optional[datetime.datetime] = None
    publication_date: Optional[datetime.datetime] = None
    quantity: Optional[str] = None
    category_en: CategoryEnum = CategoryEnum.OTHER
    is_raw: Optional[bool] = None
    brands: List[str] = []
    brand_owner: Optional[str] = None
    food_groups_en: List[str] = []
    ingredients: Optional[Ingredients] = None
    serving_size: Optional[float] = None
    serving_size_unit: Optional[str] = None
    nutrition_facts: Optional[NutritionFacts] = None
    nutriscore_data: Optional[NutriscoreData] = NutriscoreData()
    ecoscore_data: Optional[EcoscoreData] = EcoscoreData()
    nova_data: Optional[NovaData] = NovaData()

    def has_atleast_one_score(self) -> bool:
        return self.product_name is not None and (
            self.nutriscore_data.score is not None
            or self.ecoscore_data.score is not None
            or self.nova_data.score is not None
        )
