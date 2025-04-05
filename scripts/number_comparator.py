class NumberComparator:
    """
    This is a class that compares given numbers.

    Methods:
        is_same_number(first_value, second_value): Returns True if the given numbers have the same value, False otherwise
        check_value_per_100g(first_value, first_value_portion, second_value, second_value_portion): Returns True if the given values have the same value per
        100g, False otherwise
    """

    def is_same_number(self, value, second_value, tolerance=0.1):
        return (
            abs(value - second_value) <= max(abs(value), abs(second_value)) * tolerance
        )

    @staticmethod
    def replace_null_string(off_field: float, fdc_field: float) -> float:
        if off_field is None and fdc_field is not None:
            return fdc_field
        return off_field
