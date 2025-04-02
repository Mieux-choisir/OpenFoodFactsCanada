from domain.product.complexFields.production_system import ProductionSystem


class ProductionSystemMapper:
    """
    This is a class that maps products values to ProductionSystem objects.

    Methods:
        map_off_row_to_production_system(row, header): Maps the given csv row to a ProductionSystem object
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

    @staticmethod
    def map_off_row_to_production_system(
        row: list[str], header: list[str]
    ) -> ProductionSystem:
        """Maps the values in a given OFF (csv) product to a ProductionSystem object containing:
        - labels: the labels associated with the product
        - value
        - warning"""
        labels_index = header.index("labels")

        return ProductionSystem(
            labels=list(filter(None, map(str.strip, row[labels_index].split(",")))),
            value=None,
            warning=None,
        )
