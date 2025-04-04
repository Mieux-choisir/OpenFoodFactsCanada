class NumberComparator:
    """
    This is a class that compares given numbers.

    Methods:
        is_same_number(first_value, second_value): Returns True if the given numbers have the same value, False otherwise
        check_value_per_100g(first_value, first_value_portion, second_value, second_value_portion): Returns True if the given values have the same value per
        100g, False otherwise
    """

    @staticmethod
    def is_same_number(first_value, second_value) -> bool:
        """Returns True if the given numbers have the same value, False otherwise"""
        return first_value == second_value

    def check_value_per_100g(
        self, first_value, first_value_portion, second_value, second_value_portion
    ) -> bool:
        """Returns True if the given values have the same value per 100g, False otherwise"""
        portion_value = first_value * 100 / first_value_portion
        portion_second_value = second_value * 100 / second_value_portion

        return self.is_same_number(portion_value, portion_second_value)
