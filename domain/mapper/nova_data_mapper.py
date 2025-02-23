from domain.product.complexFields.nova_data import NovaData


class NovaDataMapper:

    @staticmethod
    def map_off_row_to_nova_data(row: list[str], header: list[str]) -> NovaData:
        score_field = header.index("nova_group")

        return NovaData(
            score=int(row[score_field]) if row[score_field] else None, group_markers={}
        )

    @staticmethod
    def map_off_dict_to_nova_data(product_dict: dict) -> NovaData:
        score_field = "nova_group"

        return NovaData(
            score=int(product_dict[score_field]) if product_dict[score_field] else None,
            group_markers={},
        )
