from domain.product.complexFields.production_system import ProductionSystem


class ProductionSystemMapper:
    """
    This is a class that maps products values to ProductionSystem objects.

    Methods:
        map_off_dict_to_production_system(product_dict): Maps the given dictionary to a ProductionSystem object
    """

    @staticmethod
    def map_off_dict_to_production_system(product_dict: dict) -> ProductionSystem:
        """Maps the values in a given OFF (jsonl) product to a ProductionSystem object containing:
        - labels: the labels associated with the product
        - value
        - warning"""
        labels_field = "labels_tags"

        return ProductionSystem(
            labels=(
                product_dict.get(labels_field)
                if product_dict.get(labels_field) is not None
                else []
            ),
            value=None,
            warning=None,
        )
