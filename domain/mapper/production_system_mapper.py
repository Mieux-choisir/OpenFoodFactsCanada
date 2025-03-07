from domain.product.complexFields.production_system import ProductionSystem


class ProductionSystemMapper:
    @staticmethod
    def map_off_dict_to_production_system(product_dict: dict) -> ProductionSystem:
        labels_field = "labels_tags"

        return ProductionSystem(
            labels=(
                product_dict[labels_field]
                if product_dict[labels_field] is not None
                else []
            ),
            value=None,
            warning=None,
        )

    @staticmethod
    def map_off_row_to_production_system(
        row: list[str], header: list[str]
    ) -> ProductionSystem:
        labels_field = header.index("labels")

        return ProductionSystem(
            labels=list(filter(None, map(str.strip, row[labels_field].split(",")))),
            value=None,
            warning=None,
        )
