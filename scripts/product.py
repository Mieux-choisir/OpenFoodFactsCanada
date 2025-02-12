# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
from enum import IntEnum
from typing import Optional, List, Dict
from pydantic import BaseModel, field_validator, Field


class EmptyStringToNoneModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class CategoryEnum(IntEnum):
    DAIRY_AND_EGG_PRODUCTS = 1
    SPICES_AND_HERBS = 2
    BABYFOODS = 3
    FATS_AND_OILS = 4
    POULTRY_PRODUCTS = 5
    SOUPS_SAUCES_AND_GRAVIES = 6
    SAUSAGES_AND_LUNCHEON_MEATS = 7
    BREAKFAST_CEREALS = 8
    FRUITS_AND_FRUIT_JUICES = 9
    PORK_PRODUCTS = 10
    VEGETABLES_AND_VEGETABLE_PRODUCTS = 11
    NUT_AND_SEED_PRODUCTS = 12
    BEEF_PRODUCTS = 13
    BEVERAGES = 14
    FINFISH_AND_SHELLFISH_PRODUCTS = 15
    LEGUMES_AND_LEGUME_PRODUCTS = 16
    LAMB_VEAL_AND_GAME = 17
    BAKED_PRODUCTS = 18
    SWEETS = 19
    CEREAL_GRAINS_AND_PASTA = 20
    FAST_FOODS = 21
    MEALS_ENTREES_AND_SIDE_DISHES = 22
    SNACKS = 23
    AMERICAN_INDIAN_ALASKA_NATIVE_FOODS = 24
    RESTAURANT_FOODS = 25
    BRANDED_FOOD_PRODUCTS_DATABASE = 26
    QUALITY_CONTROL_MATERIALS = 27
    ALCOHOLIC_BEVERAGES = 28
    OTHER = 29


class FoodCategoryModel(BaseModel):
    category_mapping: Dict[str, CategoryEnum] = Field(
        default_factory=lambda: {
            "Dairy and Egg Products": CategoryEnum.DAIRY_AND_EGG_PRODUCTS,
            "Spices and Herbs": CategoryEnum.SPICES_AND_HERBS,
            "Baby Foods": CategoryEnum.BABYFOODS,
            "Fats and Oils": CategoryEnum.FATS_AND_OILS,
            "Poultry Products": CategoryEnum.POULTRY_PRODUCTS,
            "Soups, Sauces, and Gravies": CategoryEnum.SOUPS_SAUCES_AND_GRAVIES,
            "Sausages and Luncheon Meats": CategoryEnum.SAUSAGES_AND_LUNCHEON_MEATS,
            "Breakfast Cereals": CategoryEnum.BREAKFAST_CEREALS,
            "Fruits and Fruit Juices": CategoryEnum.FRUITS_AND_FRUIT_JUICES,
            "Pork Products": CategoryEnum.PORK_PRODUCTS,
            "Vegetables and Vegetable Products": CategoryEnum.VEGETABLES_AND_VEGETABLE_PRODUCTS,
            "Nut and Seed Products": CategoryEnum.NUT_AND_SEED_PRODUCTS,
            "Beef Products": CategoryEnum.BEEF_PRODUCTS,
            "Beverages": CategoryEnum.BEVERAGES,
            "Finfish and Shellfish Products": CategoryEnum.FINFISH_AND_SHELLFISH_PRODUCTS,
            "Legumes and Legume Products": CategoryEnum.LEGUMES_AND_LEGUME_PRODUCTS,
            "Lamb, Veal, and Game": CategoryEnum.LAMB_VEAL_AND_GAME,
            "Baked Products": CategoryEnum.BAKED_PRODUCTS,
            "Sweets": CategoryEnum.SWEETS,
            "Cereal Grains and Pasta": CategoryEnum.CEREAL_GRAINS_AND_PASTA,
            "Fast Foods": CategoryEnum.FAST_FOODS,
            "Meals, Entrees, and Side Dishes": CategoryEnum.MEALS_ENTREES_AND_SIDE_DISHES,
            "Snacks": CategoryEnum.SNACKS,
            "American Indian/Alaska Native Foods": CategoryEnum.AMERICAN_INDIAN_ALASKA_NATIVE_FOODS,
            "Restaurant Foods": CategoryEnum.RESTAURANT_FOODS,
            "Branded Food Products Database": CategoryEnum.BRANDED_FOOD_PRODUCTS_DATABASE,
            "Quality Control Materials": CategoryEnum.QUALITY_CONTROL_MATERIALS,
            "Alcoholic Beverages": CategoryEnum.ALCOHOLIC_BEVERAGES,
            "Other": CategoryEnum.OTHER,
        }
    )

    def get_category(self, raw_category: str) -> CategoryEnum:
        return self.category_mapping.get(  # pylint: disable=no-member
            raw_category, CategoryEnum.OTHER
        )

    def get_category_name(self, category: CategoryEnum) -> str:
        for key, value in self.category_mapping.items():  # pylint: disable=no-member
            if value == category:
                return key
        return "Other"

    class Config:
        use_enum_values = True


class Ingredients(EmptyStringToNoneModel):
    ingredients_text: Optional[str] = None
    ingredients_list: List[str] = []


class NutrientLevel(EmptyStringToNoneModel):
    fat: Optional[float] = None
    salt: Optional[float] = None
    saturated_fats: Optional[float] = None
    sugar: Optional[float] = None


class Nutrients(EmptyStringToNoneModel):
    carbohydrates_100g: Optional[float] = None
    energy_100g: Optional[float] = None
    energy_kcal_100g: Optional[float] = None
    vitamin_a_100g: Optional[float] = None


class NutritionFacts(EmptyStringToNoneModel):
    nutrient_level: NutrientLevel
    nutrients: Nutrients


class NutriscoreData(EmptyStringToNoneModel):
    energy: Optional[float] = None
    fibers: Optional[float] = None
    proteins: Optional[float] = None
    saturated_fats: Optional[float] = None
    sodium: Optional[float] = None
    sugar: Optional[float] = None
    fruit_percentage: Optional[float] = 0.0
    is_beverage: Optional[bool] = False
    score: Optional[int] = None


class OriginOfIngredients(EmptyStringToNoneModel):
    origin: Optional[str] = None
    percent: Optional[int] = None
    transportation_score: Optional[str] = None


class Packaging(EmptyStringToNoneModel):
    non_recyclable_and_non_biodegradable_materials: Optional[int] = None
    packaging: List = []


class ProductionSystem(EmptyStringToNoneModel):
    labels: List = []
    value: Optional[int] = None
    warning: Optional[str] = None


class EcoscoreData(EmptyStringToNoneModel):
    score: Optional[int] = None
    origin_of_ingredients: List[OriginOfIngredients] = []
    packaging: Optional[Packaging] = None
    production_system: Optional[ProductionSystem] = None
    threatened_species: Dict = {}


class NovaData(EmptyStringToNoneModel):
    score: Optional[int] = None
    group_markers: Dict[str, List] = {}


class Product(EmptyStringToNoneModel):
    id: Optional[str] = None
    generic_name_en: Optional[str] = None
    product_name: Optional[str] = None
    category_en: CategoryEnum = CategoryEnum.OTHER
    is_raw: Optional[bool] = None
    brands: List[str]
    brand_owner: Optional[str] = None
    food_groups_en: List[str] = []
    ingredients: Optional[Ingredients] = None
    nutrition_facts: Optional[NutritionFacts] = None
    allergens: List = []
    nutriscore_data: Optional[NutriscoreData] = NutriscoreData()
    ecoscore_data: Optional[EcoscoreData] = EcoscoreData()
    nova_data: Optional[NovaData] = NovaData()

    def has_atleast_one_score(self) -> bool:
        return self.product_name is not None and (
            self.nutriscore_data.score is not None
            or self.ecoscore_data.score is not None
            or self.nova_data.score is not None
        )
