class Converter:

    @staticmethod
    def safe_int(string: str) -> int:
        """Returns the string converted to an integer if it is possible, None otherwise"""
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def safe_float(variable_to_convert: str) -> float:
        """Returns the string converted to a float if it is possible, None otherwise"""
        try:
            return float(variable_to_convert)
        except ValueError:
            return None
