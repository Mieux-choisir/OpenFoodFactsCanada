from domain.product.complexFields.packaging import Packaging


class PackagingMapper:
    """
    This is a class that maps products values to Packaging objects.

    Methods:
        map_off_dict_to_packaging(product_dict): Maps the given dictionary to a Packaging object
    """

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
