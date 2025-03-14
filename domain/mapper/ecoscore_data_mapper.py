from domain.mapper.ingredients_origin_mapper import IngredientsOriginMapper
from domain.mapper.packaging_mapper import PackagingMapper
from domain.mapper.production_system_mapper import ProductionSystemMapper
from domain.product.complexFields.ingredients_origin import IngredientsOrigin
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.utils.converter import Converter


class EcoscoreDataMapper:
    @staticmethod
    def map_off_row_to_ecoscore_data(row: list[str], header: list[str]) -> EcoscoreData:
        score_index = header.index("environmental_score_score")

        origin_of_ingredients: list[IngredientsOrigin] = [
            IngredientsOriginMapper.map_off_row_to_ingredients_origin(row, header)
        ]
        packaging = PackagingMapper.map_off_row_to_packaging(row, header)
        production_system = ProductionSystemMapper.map_off_row_to_production_system(
            row, header
        )

        return EcoscoreData(
            score=Converter.safe_int(row[score_index]) if row[score_index] else None,
            origin_of_ingredients=origin_of_ingredients,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )

    @staticmethod
    def map_off_dict_to_ecoscore_data(product_dict: dict) -> EcoscoreData:
        score_field = "environmental_score_score"

        origin_of_ingredients: list[IngredientsOrigin] = [
            IngredientsOriginMapper.map_off_dict_to_ingredients_origin(product_dict)
        ]
        packaging = PackagingMapper.map_off_dict_to_packaging(product_dict)
        production_system = ProductionSystemMapper.map_off_dict_to_production_system(
            product_dict
        )

        return EcoscoreData(
            score=(
                int(product_dict.get(score_field))
                if product_dict.get(score_field)
                else None
            ),
            origin_of_ingredients=origin_of_ingredients,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )
