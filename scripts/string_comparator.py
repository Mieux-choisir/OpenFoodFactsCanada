import re
import unicodedata
from typing import List


class StringComparator:
    @staticmethod
    def is_identical(field: str, second_field: str) -> bool:
        return field == second_field

    @staticmethod
    def is_identical_case_insensitive(self, field: str, second_field: str) -> bool:
        lower_field = field.lower()
        second_lower_field = second_field.lower()

        return self.is_identical(lower_field, second_lower_field)

    @staticmethod
    def is_identical_case_white_space(self, field: str, second_field: str) -> bool:
        white_space_field = re.sub(r"\s+", "", field)
        white_space_second_field = re.sub(r"\s+", "", second_field)

        return self.is_identical_case_insensitive(
            white_space_field, white_space_second_field
        )

    @staticmethod
    def compare_string(self, field: str, second_field: str) -> bool:
        normalized_field = "".join(
            c
            for c in unicodedata.normalize("NFD", field)
            if unicodedata.category(c) != "Mn"
        )
        normalized_second_field = "".join(
            c
            for c in unicodedata.normalize("NFD", second_field)
            if unicodedata.category(c) != "Mn"
        )

        return self.is_identical_case_white_space(
            normalized_field, normalized_second_field
        )

    @staticmethod
    def is_list_same_length(first_list: List[str], second_list: List[str]) -> bool:
        return len(first_list) == len(second_list)

    @staticmethod
    def is_lists_have_same_elements(
        self, first_list: List[str], second_list: List[str]
    ) -> bool:
        for i in range(len(first_list)):
            if not self.compare_string(first_list[i], second_list[i]):
                return False
        return True

    @staticmethod
    def compare_list(self, first_list: List[str], second_list: List[str]):
        return self.is_list_same_length(
            first_list, second_list
        ) and self.is_lists_have_same_elements(first_list, second_list)
