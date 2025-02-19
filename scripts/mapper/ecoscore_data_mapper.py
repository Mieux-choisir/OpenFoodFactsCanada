from scripts.mapper.ingredients_origin_mapper import IngredientsOriginMapper
from scripts.mapper.packaging_mapper import PackagingMapper
from scripts.mapper.production_system_mapper import ProductionSystemMapper
from scripts.product.complexFields.ingredients_origin import IngredientsOrigin
from scripts.product.complexFields.packaging import Packaging
from scripts.product.complexFields.production_system import ProductionSystem
from scripts.product.complexFields.score.ecoscore_data import EcoscoreData


class EcoscoreDataMapper:
    @staticmethod
    def map_fdc_dict_to_ecoscore_data() -> EcoscoreData:
        return EcoscoreData(
            score=None,
            origin_of_ingredients=[],
            packaging=None,
            production_system=None,
            threatened_species={},
        )

    @staticmethod
    def map_off_row_to_ecoscore_data(row: list[str], header: list[str]) -> EcoscoreData:
        score_field = header.index("environmental_score_score")

        origin_of_ingredients: list[IngredientsOrigin] = [
            IngredientsOriginMapper.map_row_to_ingredients_origin(row, header)
        ]
        packaging = PackagingMapper.map_row_to_packaging(row, header)
        production_system = ProductionSystemMapper.map_row_to_production_system(row, header)

        return EcoscoreData(
            score=int(row[score_field]) if row[score_field] else None,
            origin_of_ingredients=origin_of_ingredients,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )

    @staticmethod
    def map_off_dict_to_ecoscore_data(product_dict: dict) -> EcoscoreData:
        score_field = "environmental_score_score"

        origin_of_ingredients: list[IngredientsOrigin] = [
            IngredientsOriginMapper.map_dict_to_ingredients_origin(product_dict)
        ]
        packaging = PackagingMapper.map_dict_to_packaging(product_dict)
        production_system = ProductionSystemMapper.map_dict_to_production_system(product_dict)

        return EcoscoreData(
            score=int(product_dict[score_field]) if product_dict[score_field] else None,
            origin_of_ingredients=origin_of_ingredients,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )