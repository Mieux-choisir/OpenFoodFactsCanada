class Converter:

    @staticmethod
    def safe_int(string: str) -> int:
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def safe_float(variable_to_convert) -> float:
        try:
            return float(variable_to_convert)
        except ValueError:
            return None
