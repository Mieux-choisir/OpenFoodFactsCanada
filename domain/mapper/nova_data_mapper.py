from domain.product.complexFields.nova_data import NovaData


class NovaDataMapper:
    """
    This is a class that maps products values to NovaData objects.

    Methods:
       map_off_dict_to_nova_data(product_dict): Maps the given dictionary to a NovaData object
    """

    @staticmethod
    def map_off_dict_to_nova_data(product_dict: dict) -> NovaData:
        """Maps the values of a given OFF (jsonl) product to a NovaData object containing:
        - score: the nova group of the product
        - group_markers"""
        score_field = "nova_group"

        return NovaData(
            score=(
                int(product_dict.get(score_field))
                if isinstance(product_dict.get(score_field), int)
                else None
            ),
            group_markers={},
        )
