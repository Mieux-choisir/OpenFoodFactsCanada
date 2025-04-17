from typing import Optional, Dict, Any

from domain.product.complexFields.complex_field import ComplexField


class NutritionFactsPerHundredGrams(ComplexField):
    """
    This is a class that stores data on the nutrition facts per 100 grams of a product.

    Attributes:
        fat_100g (Optional[float]): The amount of saturated fats (g) in 100g of the product
        salt_100g (Optional[float]): The amount of saturated salt (g) in 100g of the product
        saturated_fats_100g (Optional[float]): The amount of saturated fats (g) in 100g of the product
        sugar_100g (Optional[float]): The amount of sugar (g) in 100g of the product
        carbohydrates_100g (Optional[float]): The amount of carbohydrates (g) in 100g of the product
        energy_100g (Optional[float]): The amount of energy (kJ) in 100g of the product
        energy_kcal_100g (Optional[float]): The amount of energy (kcal) in 100g of the product
        proteins_100g (Optional[float]): The amount of proteins (g) in 100g of the product
        fibers_100g (Optional[float]): The amount of fibers (g) in 100g of the product
        sodium_100g (Optional[float]): The amount of sodium (g) in 100g of the product
        monounsaturated_fats_100g (Optional[float]): The amount of monounsaturated fats (g) in 100g of the product
        polyunsaturated_fats_100g (Optional[float]): The amount of polyunsaturated fats (g) in 100g of the product
        trans_fats_100g (Optional[float]): The amount of trans fats (g) in 100g of the product
        cholesterol_100g (Optional[float]): The amount of cholesterol (g) in 100g of the product
        calcium_100g (Optional[float]): The amount of calcium (g) in 100g of the product
        iron_100g (Optional[float]): The amount of iron (g) in 100g of the product
        potassium_100g (Optional[float]): The amount of potassium (g) in 100g of the product
        vitamin_a_100g (Optional[float]): The amount of vitamin a (g) in 100g of the product
        vitamin_b1_100g (Optional[float]): The amount of vitamin b1 (g) in 100g of the product
        vitamin_b2_100g (Optional[float]): The amount of vitamin b2 (g) in 100g of the product
        vitamin_b6_100g (Optional[float]): The amount of vitamin b6 (g) in 100g of the product
        vitamin_b9_100g (Optional[float]): The amount of vitamin b9 (g) in 100g of the product
        vitamin_b12_100g (Optional[float]): The amount of vitamin b12 (g) in 100g of the product
        vitamin_c_100g (Optional[float]): The amount of vitamin c (g) in 100g of the product
        vitamin_pp_100g (Optional[float]): The amount of vitamin a pp (g) in 100g of the product
        phosphorus_100g (Optional[float]): The amount of phosphorus (g) in 100g of the product
        magnesium_100g (Optional[float]): The amount of magnesium (g) in 100g of the product
        zinc_100g (Optional[float]): The amount of zinc (g) in 100g of the product
        folates_100g (Optional[float]): The amount of folates (g) in 100g of the product
        pantothenic_acid_100g (Optional[float]): The amount of pantothenic acid (g) in 100g of the product
        soluble_fiber_100g (Optional[float]): The amount of soluble fiber (g) in 100g of the product
        insoluble_fiber_100g (Optional[float]): The amount of insoluble fiber (g) in 100g of the product
        copper_100g (Optional[float]): The amount of copper (g) in 100g of the product
        manganese_100g (Optional[float]): The amount of manganese (g) in 100g of the product
        polyols_100g (Optional[float]): The amount of polyols (g) in 100g of the product
        selenium_100g (Optional[float]): The amount of selenium (g) in 100g of the product
        phylloguinone_100g (Optional[float]): The amount of phylloguinone (g) in 100g of the product
        iodine_100g (Optional[float]): The amount of iodine (g) in 100g of the product
        biotin_100g (Optional[float]): The amount of biotin (g) in 100g of the product
        caffeine_100g (Optional[float]): The amount of caffeine (g) in 100g of the product
        molybdenum_100g (Optional[float]): The amount of molybdenum (g) in 100g of the product
        chromium_100g (Optional[float]): The amount of chromium (g) in 100g of the product
    """

    fat_100g: Optional[float] = None
    salt_100g: Optional[float] = None
    saturated_fats_100g: Optional[float] = None
    sugar_100g: Optional[float] = None
    carbohydrates_100g: Optional[float] = None
    energy_100g: Optional[float] = None
    energy_kcal_100g: Optional[float] = None
    proteins_100g: Optional[float] = None
    fibers_100g: Optional[float] = None
    sodium_100g: Optional[float] = None
    monounsaturated_fats_100g: Optional[float] = None
    polyunsaturated_fats_100g: Optional[float] = None
    trans_fats_100g: Optional[float] = None
    cholesterol_100g: Optional[float] = None
    calcium_100g: Optional[float] = None
    iron_100g: Optional[float] = None
    potassium_100g: Optional[float] = None
    vitamin_a_100g: Optional[float] = None
    vitamin_b1_100g: Optional[float] = None
    vitamin_b2_100g: Optional[float] = None
    vitamin_b6_100g: Optional[float] = None
    vitamin_b9_100g: Optional[float] = None
    vitamin_b12_100g: Optional[float] = None
    vitamin_c_100g: Optional[float] = None
    vitamin_pp_100g: Optional[float] = None
    phosphorus_100g: Optional[float] = None
    magnesium_100g: Optional[float] = None
    zinc_100g: Optional[float] = None
    folates_100g: Optional[float] = None
    pantothenic_acid_100g: Optional[float] = None
    soluble_fiber_100g: Optional[float] = None
    insoluble_fiber_100g: Optional[float] = None
    copper_100g: Optional[float] = None
    manganese_100g: Optional[float] = None
    polyols_100g: Optional[float] = None
    selenium_100g: Optional[float] = None
    phylloguinone_100g: Optional[float] = None
    iodine_100g: Optional[float] = None
    biotin_100g: Optional[float] = None
    caffeine_100g: Optional[float] = None
    molybdenum_100g: Optional[float] = None
    chromium_100g: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NutritionFactsPerHundredGrams":
        if not data:
            return cls()
        return cls(
            fat_100g=data.get("fat_100g"),
            salt_100g=data.get("salt_100g"),
            saturated_fats_100g=data.get("saturated_fats_100g"),
            sugar_100g=data.get("sugar_100g"),
            carbohydrates_100g=data.get("carbohydrates_100g"),
            energy_100g=data.get("energy_100g"),
            energy_kcal_100g=data.get("energy_kcal_100g"),
            proteins_100g=data.get("proteins_100g"),
            fibers_100g=data.get("fibers_100g"),
            sodium_100g=data.get("sodium_100g"),
            monounsaturated_fats_100g=data.get("monounsaturated_fats_100g"),
            polyunsaturated_fats_100g=data.get("polyunsaturated_fats_100g"),
            trans_fats_100g=data.get("trans_fats_100g"),
            cholesterol_100g=data.get("cholesterol_100g"),
            calcium_100g=data.get("calcium_100g"),
            iron_100g=data.get("iron_100g"),
            potassium_100g=data.get("potassium_100g"),
            vitamin_a_100g=data.get("vitamin_a_100g"),
            vitamin_b1_100g=data.get("vitamin_b1_100g"),
            vitamin_b2_100g=data.get("vitamin_b2_100g"),
            vitamin_b6_100g=data.get("vitamin_b6_100g"),
            vitamin_b9_100g=data.get("vitamin_b9_100g"),
            vitamin_b12_100g=data.get("vitamin_b12_100g"),
            vitamin_c_100g=data.get("vitamin_c_100g"),
            vitamin_pp_100g=data.get("vitamin_pp_100g"),
            phosphorus_100g=data.get("phosphorus_100g"),
            magnesium_100g=data.get("magnesium_100g"),
            zinc_100g=data.get("zinc_100g"),
            folates_100g=data.get("folates_100g"),
            pantothenic_acid_100g=data.get("pantothenic_acid_100g"),
            soluble_fiber_100g=data.get("soluble_fiber_100g"),
            insoluble_fiber_100g=data.get("insoluble_fiber_100g"),
            copper_100g=data.get("copper_100g"),
            manganese_100g=data.get("manganese_100g"),
            polyols_100g=data.get("polyols_100g"),
            selenium_100g=data.get("selenium_100g"),
            phylloguinone_100g=data.get("phylloguinone_100g"),
            iodine_100g=data.get("iodine_100g"),
            biotin_100g=data.get("biotin_100g"),
            caffeine_100g=data.get("caffeine_100g"),
            molybdenum_100g=data.get("molybdenum_100g"),
            chromium_100g=data.get("chromium_100g"),
        )
