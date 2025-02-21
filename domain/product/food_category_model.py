from typing import Dict

from pydantic import BaseModel, Field

from domain.product.category_enum import CategoryEnum


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
