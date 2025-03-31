class NumberComparator:
    def is_same_number(self, value, second_value, tolerance=0.1):
        return abs(value - second_value) <= max(abs(value), abs(second_value)) * tolerance
    @staticmethod
    def replace_null_string(off_field: float, fdc_field: float) -> float:
        if off_field is None and fdc_field is not None:
            return fdc_field
        return off_field
