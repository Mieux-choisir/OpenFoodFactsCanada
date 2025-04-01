from domain.product.complexFields.packaging import Packaging


class PackagingMapper:
    @staticmethod
    def map_off_row_to_packaging(row: list[str], header: list[str]) -> Packaging:
        """Maps the values in a given OFF (csv) product to a Packaging object containing:
        - non_recyclable_and_non_biodegradable_materials: the number of non-recyclable or non-biodegradable materials used in the package of the product
        - packaging: the list of materials used in the package"""
        packaging_index = header.index("packaging")

        return Packaging(
            non_recyclable_and_non_biodegradable_materials=None,
            packaging=list(
                filter(None, map(str.strip, row[packaging_index].split(",")))
            ),
        )

    @staticmethod
    def map_off_dict_to_packaging(product_dict: dict) -> Packaging:
        """Maps the values in a given OFF (jsonl) product to a Packaging object containing:
        - non_recyclable_and_non_biodegradable_materials: the number of non-recyclable or non-biodegradable materials used in the package of the product
        - packaging: the list of materials used in the package"""
        packaging_tags_field = "packaging_tags"

        return Packaging(
            non_recyclable_and_non_biodegradable_materials=None,
            packaging=(
                product_dict.get(packaging_tags_field)
                if product_dict.get(packaging_tags_field) is not None
                else []
            ),
        )
