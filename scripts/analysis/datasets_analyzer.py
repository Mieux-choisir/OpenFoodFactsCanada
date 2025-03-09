import logging
import csv
import json
import ijson

from scripts.analysis.fields_types_analyzer import FieldsTypesAnalyzer


def analyze_off_csv_data(
    filename: str, nonetype_included: bool, limit: int = None
) -> (dict, set):
    """Analyzes and counts the different types appearing in each field of the CSV dataset.
    Args:
        filename (str): the path of the CSV file
        nonetype_included (bool): whether the None values are counted and presented in the analysis
        limit (int): the number of products (ie lines in the csv) to analyze
    Returns:
        (fields_types, fields_none) (dict, set):
            - fields_types: a dict that contains the types appearing and the number of their occurrences for each field
            - fields_none: the set of fields that can have the value None"""
    if limit is not None:
        logging.info(
            f"Analyzing the data of {limit} products from Open Food Facts csv dataset..."
        )
    else:
        logging.info(
            "Analyzing the data of all products from Open Food Facts csv dataset..."
        )

    # Increase the CSV field size limit to avoid the error:
    # _csv.Error: field larger than field limit (131072)
    csv.field_size_limit(2**30)

    n = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        fields_types = {}
        fields_can_be_none = set()

        for row in reader:
            for field_index in range(len(header)):
                field, field_value = header[field_index], row[field_index]

                fields_analyzer = FieldsTypesAnalyzer()
                field_type = fields_analyzer.get_field_type(field, field_value)

                if nonetype_included or field_type != "NoneType":
                    if field not in fields_types.keys():
                        fields_types[field] = {field_type: 1}
                    elif field_type not in fields_types[field].keys():
                        fields_types[field][field_type] = 1
                    else:
                        fields_types[field][field_type] += 1
                elif field not in fields_types.keys():
                    fields_types[field] = {}

                if field_type == "NoneType":
                    fields_can_be_none.add(field)

            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("OFF data analyzed.")
    __show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def analyze_off_jsonl_data(
    filename: str, nonetype_included: bool, limit: int = None
) -> (dict, set):
    """Analyzes and counts the different types appearing in each field of the jsonl dataset.
    Args:
        filename (str): the path of the CSV file
        nonetype_included (bool): whether the None values are counted and presented in the analysis
        limit (int): the number of products (ie lines in the csv) to analyze
    Returns:
        (fields_types, fields_none) (dict, set):
            - fields_types: a dict that contains the types appearing and the number of their occurrences for each field
            - fields_none: the set of fields that can have the value None"""
    if limit is not None:
        logging.info(
            f"Analyzing the data of {limit} products from Open Food Facts jsonl dataset..."
        )
    else:
        logging.info(
            "Analyzing the data of all products from Open Food Facts jsonl dataset..."
        )

    n = 0
    with open(filename, "r", encoding="utf-8") as file:
        fields_types = {}
        fields_can_be_none = set()

        for line in file:
            try:
                obj = json.loads(line.strip())

                fields_types, fields_can_be_none = __analyze_obj(
                    obj, fields_types, fields_can_be_none, nonetype_included
                )

                n += 1

                if limit is not None and n >= limit:
                    break

            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    logging.info("OFF data analyzed.")
    __show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def analyze_fdc_data(
    filename: str, nonetype_included: bool, limit: int = None
) -> (dict, set):
    """Analyzes and counts the different types appearing in each field of the json dataset.
    Args:
        filename (str): the path of the CSV file
        nonetype_included (bool): whether the None values are counted and presented in the analysis
        limit (int): the number of products (ie lines in the csv) to analyze
    Returns:
        (fields_types, fields_none) (dict, set):
            - fields_types: a dict that contains the types appearing and the number of their occurrences for each field
            - fields_none: the set of fields that can have the value None"""
    if limit is not None:
        logging.info(
            f"Analyzing the data of {limit} products from Food Data Central dataset..."
        )
    else:
        logging.info(
            "Analyzing the data of all products from Food Data Central dataset..."
        )

    n = 0

    with open(filename, "r", encoding="utf-8") as file:
        fields_types = {}
        fields_can_be_none = set()

        for obj in ijson.items(file, "BrandedFoods.item"):
            fields_types, fields_can_be_none = __analyze_obj(
                obj, fields_types, fields_can_be_none, nonetype_included
            )

            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("FDC data analyzed.")
    __show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def __analyze_obj(
    obj: dict, fields_types: dict, fields_can_be_none: set, nonetype_included: bool
) -> (dict, set):
    """Analyzes and counts the different types appearing in each field of the CSV dataset.
    Returns (updated_fields_types, updated_fields_can_be_none) (dict, set) where:
    - updated_fields_types is the updated dict that contains the types appearing and the number of their occurrences for each field
    - updated_fields_can_be_none is the new set of fields that can have the value None
    """
    for key in obj.keys():
        fields_types = __add_type_to_dict(
            fields_types, key, obj[key], nonetype_included
        )

        if obj[key] is None:
            fields_can_be_none.add(key)

    return fields_types, fields_can_be_none


def __add_type_to_dict(fields_types, key, value, nonetype_included: bool):
    """Adds the registered occurence to the fields_types dictionary that counts the appearing types for each field
    and returns the updated dictionary."""
    if nonetype_included or value is not None:
        if key not in fields_types.keys():
            fields_types[key] = {type(value).__name__: 1}
        elif not type(value).__name__ in fields_types[key].keys():
            fields_types[key][type(value).__name__] = 1
        else:
            fields_types[key][type(value).__name__] += 1
    elif key not in fields_types.keys():
        fields_types[key] = {}

    return fields_types


def __show_fields_report(fields_types: dict, fields_can_be_none: set) -> None:
    """Shows the report for the analysis of the types of each field of the dataset in two parts :
    - first it shows the appearing types and the number of their occurrences for each field in the dataset
    - them it lists all the fields in the dataset that were None at least once
    """
    types = "Analyzed fields types:"
    for field in fields_types:
        types += f"\n\t{field}: {fields_types[field]}"
    logging.info(f"{types}\n")

    possible_nonetypes = ""
    for value in fields_can_be_none:
        possible_nonetypes += f"\n\t {value}"
    logging.info(
        f"{len(fields_can_be_none)} out of {len(fields_types)} fields can be None : {possible_nonetypes}"
    )


def __show_inconsistent_fields(field_types: dict) -> None:
    """Lists all the given fields that have inconsistent types (expect for NoneType)"""
    inconsistent_fields = {}
    for field in field_types.keys():
        if len([key for key in field_types[field].keys() if key != "NoneType"]) > 1:
            inconsistent_fields[field] = list(field_types[field].keys())

    logging.info(f"Inconsistent fields: {inconsistent_fields}")


def __record_values_for_field_off_csv(
    field_name: str, show_values: bool, filename: str, limit: int = None
) -> set:
    """Keeps track of all the appearing values in a given field of a csv dataset and shows them"""
    if limit is not None:
        logging.info(
            f"Recording values from {limit} items for {field_name} field from Open Food Facts csv dataset..."
        )
    else:
        logging.info(
            f"Recording all values for {field_name} field from Open Food Facts csv dataset..."
        )

    csv.field_size_limit(2**30)

    n = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        values = set()

        for row in reader:
            idx = header.index(field_name)
            if row[idx] != "":
                values.add(row[idx])

            n += 1

            if limit is not None and n >= limit:
                break

    if show_values:
        __show_recorded_values(values, [])

    logging.info(f"values for {field_name} field recorded")
    return values


def __record_values_for_field_off_jsonl(
    field_name: str, show_values: bool, filename: str, limit: int = None
) -> set:
    """Keeps track of all the appearing values in a given field of a jsonl dataset and shows them"""
    if limit is not None:
        logging.info(
            f"Recording values from {limit} items for {field_name} field from Open Food Facts jsonl dataset..."
        )
    else:
        logging.info(
            f"Recording all values for {field_name} field from Open Food Facts jsonl dataset..."
        )

    n = 0
    with open(filename, "r", encoding="utf-8") as file:
        hashable_values = set()
        non_hashable_values = []
        for line in file:
            try:
                obj = json.loads(line.strip())
                if field_name in obj.keys():
                    value = obj[field_name]
                    if value != "" and value is not None:
                        if not isinstance(value, list) and not isinstance(value, dict):
                            hashable_values.add(value)
                        else:
                            if value not in non_hashable_values:
                                non_hashable_values.append(value)

                    n += 1

                    if limit is not None and n > limit:
                        break

            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    if show_values:
        __show_recorded_values(hashable_values, non_hashable_values)

    logging.info(f"values for {field_name} field recorded")
    return hashable_values


def __record_values_for_field_fdc(
    field_name: str, show_values: bool, filename: str, limit: int = None
) -> (set, list):
    """Keeps track of all the appearing values in a given field of a json dataset and shows them"""
    if limit is not None:
        logging.info(
            f"Recording values from {limit} items for {field_name} field from Food Data Central dataset..."
        )
    else:
        logging.info(
            f"Recording all values for {field_name} field from Food Data Central dataset..."
        )

    n = 0
    with open(filename, "r", encoding="utf-8") as file:
        hashable_values = set()
        non_hashable_values = []
        for obj in ijson.items(file, "BrandedFoods.item"):
            if field_name in obj.keys():
                value = obj[field_name]
                if value != "" and value is not None:
                    if not isinstance(value, list) and not isinstance(value, dict):
                        hashable_values.add(value)
                    else:
                        if value not in non_hashable_values:
                            non_hashable_values.append(value)

                n += 1

                if limit is not None and n >= limit:
                    break

    if show_values:
        __show_recorded_values(hashable_values, non_hashable_values)

    logging.info(f"values for {field_name} field recorded")
    return hashable_values, non_hashable_values


def __show_recorded_values(set_values: set, list_values: list) -> None:
    """Lists all the values appearing in the given set"""
    values_list = ""
    for value in set_values:
        values_list += f"\n\t{value}"
    for value in list_values:
        values_list += f"\n\t{value}"
    logging.info(f"Values found:{values_list}")
