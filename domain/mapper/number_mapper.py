class NumberMapper:
    letter_to_number_ascii_code = 96

    @staticmethod
    def map_letter_to_number(letter: str) -> int | None:
        try:
            return ord(letter.lower()) - NumberMapper.letter_to_number_ascii_code
        except TypeError:
            return None
