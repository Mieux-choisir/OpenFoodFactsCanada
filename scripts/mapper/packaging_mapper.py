from scripts.product.complexFields.packaging import Packaging


class PackagingMapper:
    @staticmethod
    def map_row_to_packaging(row: list[str], header: list[str]) -> Packaging:
        packaging_field = header.index("packaging")

        return Packaging(
            non_recyclable_and_non_biodegradable_materials=None,
            packaging=row[packaging_field].split(","),
        )

    @staticmethod
    def map_dict_to_packaging(product_dict: dict) -> Packaging:
        packaging_tags_field = "packaging_tags"

        return Packaging(
            non_recyclable_and_non_biodegradable_materials=None,
            packaging=(
                product_dict[packaging_tags_field]
                if product_dict[packaging_tags_field] is not None
                else []
            ),
        )
