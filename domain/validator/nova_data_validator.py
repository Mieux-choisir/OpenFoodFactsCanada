class NovaDataValidator:
    @staticmethod
    def check_nova_raw_group(nova_group: str) -> bool:
        """Checks if the given nova group string is valid and returns True if it is a group of raw foods, False otherwise"""
        if nova_group and nova_group != "":
            try:
                nova_value = int(nova_group)
                if nova_value == 1:
                    return True
                return False
            except ValueError:
                raise ValueError
        return False

    @staticmethod
    def check_nova_transformed_group(nova_group: str) -> bool:
        """Checks if the given nova group string is valid and returns True if it is a group of ultra transformed foods,
        False otherwise"""
        if nova_group and nova_group != "":
            try:
                nova_value = int(nova_group)
                if nova_value == 4:
                    return True
                return False
            except ValueError:
                raise ValueError
        return False
