import datetime


class FieldsTypesAnalyzer:

    def get_field_type(self, field: str, field_value: str) -> str:
        """Returns the type corresponding to the value in the given string"""
        field_type = self.__get_particular_cases_type(field, field_value)

        if not field_type:
            field_type = type(None).__name__

            if self.__value_is_int(field_value):
                field_type = int.__name__
            elif self.__value_is_float(field_value):
                field_type = float.__name__
            elif self.__value_is_list(field_value):
                field_type = list.__name__
            elif self.__value_is_string(field_value):
                field_type = str.__name__

        return field_type

    @staticmethod
    def __get_particular_cases_type(field: str, field_value: str) -> str | None:
        """Returns the type of the value given in the string if it matches any particular case, else returns None"""
        if field_value == "":
            return type(None).__name__
        if field == "code" or "_name" in field:
            return str.__name__
        if "_tags" in field:
            return list.__name__
        if "_100g" in field:
            return float.__name__
        if "_t" in field[:-2]:
            return int.__name__
        if "_datetime" in field:
            return datetime.__name__
        return None

    @staticmethod
    def __value_is_float(field_value: str) -> bool:
        """Checks if the given value in the string is a float number"""
        is_float = False
        try:
            float(field_value)
            is_float = True
        except ValueError:
            pass
        return is_float

    @staticmethod
    def __value_is_int(field_value: str) -> bool:
        """Checks if the given value in the string is an integer"""
        return field_value.isdigit()

    @staticmethod
    def __value_is_list(field_value: str) -> bool:
        """Checks if the given value in the string is a list"""
        return "," in field_value

    @staticmethod
    def __value_is_string(field_value: str) -> bool:
        """Checks if the given value in the string is a non-empty string"""
        return field_value != ""
