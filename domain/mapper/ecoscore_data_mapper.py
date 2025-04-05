from domain.mapper.ingredients_origins_mapper import IngredientsOriginMapper
from domain.mapper.packaging_mapper import PackagingMapper
from domain.mapper.production_system_mapper import ProductionSystemMapper
from domain.product.complexFields.ingredients_origins import IngredientsOrigins
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.utils.converter import Converter


class EcoscoreDataMapper:
    """
    This is a class that maps products values to EcoscoreData objects.

    Methods:
        map_off_row_to_ecoscore_data(row, header): Maps the given csv row to an EcoscoreData object
        map_off_dict_to_ecoscore_data(product_dict): Maps the given dictionary to an EcoscoreData object
    """

    @staticmethod
    def map_off_row_to_ecoscore_data(row: list[str], header: list[str]) -> EcoscoreData:
        """Maps the values in a given OFF (csv) product to an EcoscoreData object"""
        score_index = header.index("environmental_score_score")

        ingredients_origins: IngredientsOrigins = (
            IngredientsOriginMapper.map_off_row_to_ingredients_origin(row, header)
        )
        packaging = PackagingMapper.map_off_row_to_packaging(row, header)
        production_system = ProductionSystemMapper.map_off_row_to_production_system(
            row, header
        )

        return EcoscoreData(
            score=Converter.safe_int(row[score_index]) if row[score_index] else None,
            ingredients_origins=ingredients_origins,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )

    @staticmethod
    def map_off_dict_to_ecoscore_data(product_dict: dict) -> EcoscoreData:
        """Maps the values in a given OFF (jsonl) product to an EcoscoreData object"""
        score_field = "environmental_score_score"

        ingredients_origins: IngredientsOrigins = (
            IngredientsOriginMapper.map_off_dict_to_ingredients_origin(product_dict)
        )
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
            ingredients_origins=ingredients_origins,
            packaging=packaging,
            production_system=production_system,
            threatened_species={},
        )
