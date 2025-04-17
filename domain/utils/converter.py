class Converter:
    """
    This is a class that converts strings to different types.

    Methods:
        safe_int(string):  Converts a string to an integer if possible
        safe_float(string): Converts a string to a float if possible
    """

    @staticmethod
    def safe_int(string: str) -> int:
        """Returns the string converted to an integer if it is possible, None otherwise"""
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def safe_float(variable_to_convert: str) -> float | None:
        """Returns the string converted to a float if it is possible, None otherwise"""
        try:
            return float(variable_to_convert)
        except (ValueError, TypeError):
            return None
