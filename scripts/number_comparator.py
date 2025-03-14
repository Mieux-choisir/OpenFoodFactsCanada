class NumberComparator:
    def is_same_number(self, value, second_value):
        return value == second_value

    def check_value_per_100g(
        self, value, value_portion, second_value, second_value_portion
    ):
        portion_value = value * 100 / value_portion
        portion_second_value = second_value * 100 / second_value_portion

        return self.is_same_number(portion_value, portion_second_value)
