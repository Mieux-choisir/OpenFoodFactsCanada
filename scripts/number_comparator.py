class NumberComparator:
    def is_same_number(self, value, second_value, tolerance=0.01):
        return abs(value - second_value) <= max(abs(value), abs(second_value)) * tolerance

    def check_value_per_100g(
        self, value, value_portion, second_value, second_value_portion
    ):
        portion_value = value * 100 / value_portion
        portion_second_value = second_value * 100 / second_value_portion

        return self.is_same_number(portion_value, portion_second_value)
    @staticmethod
    def replace_null_string(off_field: float, fdc_field: float) -> float:
        if off_field is None and fdc_field is not None:
            return fdc_field
        return off_field
