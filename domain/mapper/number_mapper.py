class NumberMapper:
    """
    This is a class that maps products values to Ingredients objects.

    Attributes:
       letter_to_number_ascii_code (int)

    Methods:
        map_letter_to_number(letter): Maps the given letter string to its corresponding alphabetical number
    """

    letter_to_number_ascii_code = 96

    @staticmethod
    def map_letter_to_number(letter: str) -> int | None:
        """Maps a given letter to its corresponding alphabetical number"""
        if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
            return None

        return ord(letter.lower()) - NumberMapper.letter_to_number_ascii_code
