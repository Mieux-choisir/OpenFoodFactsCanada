class Converter:

    @staticmethod
    def safe_int(string: str) -> int:
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def safe_float(string: str) -> float:
        try:
            return float(string)
        except ValueError:
            return None
