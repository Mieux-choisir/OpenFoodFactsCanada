import csv
import logging
import os

from pymongo import MongoClient


class StatisticsCreator:
    def make_merge_summary(
        self,
        overwrite_counter,
        complete_counter,
        count_skipped,
        count_off_products,
        count_fdc_products,
    ):
        logging.info("=== Merge Summary ===")

        compute_percentages = True
        if count_off_products != count_fdc_products:
            logging.warning(
                f"Number of products in matched collections does not match between OFF ({count_off_products}) and FDC ({count_fdc_products})."
                f"Cannot compute make percentages."
            )
            compute_percentages = False

        self.__make_overwritten_summary(
            overwrite_counter, count_off_products, compute_percentages
        )
        self.__make_completed_summary(
            complete_counter, count_off_products, compute_percentages
        )
        self.__make_skipped_summary(
            count_skipped, count_off_products, compute_percentages
        )

    def compare_number_differences(self, threshold=0.1, use_docker=True):
        print("Starting statistics comparison ...")
        _, off_cursor, _, final_cursor = self.__get_products(use_docker)

        off_product = next(off_cursor, None)
        final_product = next(final_cursor, None)

        fields_differences_count = {}
        not_updated = 0

        fields_to_check = ["serving_size"]
        fields_with_subfields_to_check = [
            "nutriscore_data",
            "nutrition_facts.nutrition_facts_per_hundred_grams",
            "nutrition_facts.nutrition_facts_per_serving",
        ]

        while off_product and final_product:
            for field in fields_to_check:
                fields_differences_count = self.__count_for_field(
                    fields_differences_count,
                    field,
                    off_product.get(field),
                    final_product.get(field),
                    threshold,
                )

            for field in fields_with_subfields_to_check:
                full_field = field
                wanted_field = field.split(".")
                off_document = off_product
                final_document = final_product

                for subfield in wanted_field:
                    off_document = off_document.get(subfield)
                    final_document = final_document.get(subfield)

                if off_document is not None and final_document is not None:
                    for subfield in (
                        k for k in off_document.keys() if k != "is_beverage"
                    ):
                        fields_differences_count = self.__count_for_field(
                            fields_differences_count,
                            full_field + "." + subfield,
                            off_document.get(subfield),
                            final_document.get(subfield),
                            threshold,
                        )
                elif final_document is not None:
                    for subfield in (
                        k for k in final_document.keys() if k != "is_beverage"
                    ):
                        fields_differences_count = self.__count_for_field(
                            fields_differences_count,
                            full_field + "." + subfield,
                            None,
                            final_document.get(subfield),
                            threshold,
                        )
                else:
                    not_updated += 1
            off_product = next(off_cursor, None)
            final_product = next(final_cursor, None)

        print("not updated: ", not_updated)
        for key in fields_differences_count.keys():
            values = fields_differences_count.get(key)
            total = (
                values.get("completed")
                + values.get("modified_above_threshold")
                + values.get("modified_below_threshold")
                + values.get("same_value")
            )
            print(
                key,
                f"\n\tCompleted: {values.get("completed")} [{round(values.get("completed") * 100 / total, 2)}%]"
                + f"\n\tAbove threshold: {values.get("modified_above_threshold")} [{round(values.get("modified_above_threshold") * 100 / total, 2)}%]"
                + f"\n\tBelow threshold: {values.get("modified_below_threshold")} [{round(values.get("modified_below_threshold") * 100 / total, 2)}%]"
                + f"\n\tSame value: {values.get("same_value")} [{round(values.get("same_value") * 100 / total, 2)}%]",
            )

        return fields_differences_count

    def __count_for_field(
        self, fields_differences_count, field, off_value, final_value, threshold
    ):
        if off_value is None and final_value is not None:
            fields_differences_count = self.__update_absent_counts(
                fields_differences_count, field
            )
        elif (
            off_value is not None
            and final_value is not None
            and abs(off_value - final_value) >= threshold
        ):
            fields_differences_count = self.__update_modified_above_threshold_counts(
                fields_differences_count, field
            )
        elif (
            off_value is not None
            and final_value is not None
            and abs(off_value - final_value) > 0
        ):
            fields_differences_count = self.__update_modified_below_threshold_counts(
                fields_differences_count, field
            )
        else:
            fields_differences_count = self.__update_same_value_counts(
                fields_differences_count, field
            )
        return fields_differences_count

    @staticmethod
    def __update_absent_counts(fields_differences_count, field):
        if field not in fields_differences_count.keys():
            fields_differences_count[field] = {
                "completed": 0,
                "modified_above_threshold": 0,
                "modified_below_threshold": 0,
                "same_value": 0,
            }
        fields_differences_count.get(field)["completed"] += 1
        return fields_differences_count

    @staticmethod
    def __update_modified_above_threshold_counts(fields_differences_count, field):
        if field not in fields_differences_count.keys():
            fields_differences_count[field] = {
                "completed": 0,
                "modified_above_threshold": 0,
                "modified_below_threshold": 0,
                "same_value": 0,
            }
        fields_differences_count.get(field)["modified_above_threshold"] += 1
        return fields_differences_count

    @staticmethod
    def __update_modified_below_threshold_counts(fields_differences_count, field):
        if field not in fields_differences_count.keys():
            fields_differences_count[field] = {
                "completed": 0,
                "modified_above_threshold": 0,
                "modified_below_threshold": 0,
                "same_value": 0,
            }
        fields_differences_count.get(field)["modified_below_threshold"] += 1
        return fields_differences_count

    @staticmethod
    def __update_same_value_counts(fields_differences_count, field):
        if field not in fields_differences_count.keys():
            fields_differences_count[field] = {
                "completed": 0,
                "modified_above_threshold": 0,
                "modified_below_threshold": 0,
                "same_value": 0,
            }
        fields_differences_count.get(field)["same_value"] += 1
        return fields_differences_count

    @staticmethod
    def __make_overwritten_summary(overwrite_counter, count_total, compute_percentages):
        logging.info("Most overwritten fields:")
        for field, count in overwrite_counter.most_common():
            message = f"  {field}: {count} times"
            if compute_percentages:
                message += f" [{round(count * 100 / count_total, 2)}%]"
            logging.info(message)

    @staticmethod
    def __make_completed_summary(complete_counter, count_total, compute_percentages):
        logging.info("Most completed fields:")
        for field, count in complete_counter.most_common():
            message = f"  {field}: {count} times"
            if compute_percentages:
                message += f" [{round(count * 100 / count_total, 2)}%]"
            logging.info(message)

    @staticmethod
    def __make_skipped_summary(count_skipped, count_total, compute_percentages):
        message = f"Total skipped products: {count_skipped}"
        if compute_percentages:
            message += f" [{round(count_skipped * 100 / count_total, 2)}%]"
        logging.info(message)

    def create_csv_modification_report(self, use_docker=True):
        parent_dir, off_cursor, fdc_cursor, final_cursor = self.__get_products(
            use_docker
        )

        off_product = next(off_cursor, None)
        fdc_product = next(fdc_cursor, None)
        final_product = next(final_cursor, None)

        csv_file = os.path.join(parent_dir, "data", "modifications.csv")
        logging.info(f"Creating csv file: {csv_file}")
        with open(csv_file, "w", encoding="utf-8", newline="") as file:
            filewriter = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            columns = ["id", "field_name", "value_off", "value_final", "value_fdc"]
            filewriter.writerow(columns)
            nb_products = 0
            while off_product and fdc_product and final_product:
                nb_products += 1
                self.__write_modified_values(
                    filewriter,
                    off_product.get("id_match"),
                    off_product,
                    fdc_product,
                    final_product,
                )
                if nb_products >= 500:
                    return
                off_product = next(off_cursor, None)
                fdc_product = next(fdc_cursor, None)
                final_product = next(final_cursor, None)
            logging.info("Csv file created!")

    def __write_modified_values(
        self, filewriter, product_id, off, fdc, final, parent_key=""
    ):
        if (
            not isinstance(off, dict)
            or not isinstance(fdc, dict)
            or not isinstance(final, dict)
        ):
            pass

        for key in set(off.keys()).union(fdc.keys()).union(final.keys()):
            full_key = f"{parent_key}.{key}" if parent_key else key
            off_value = off.get(key)
            fdc_value = fdc.get(key)
            final_value = final.get(key)

            if (
                isinstance(off_value, dict)
                and isinstance(fdc_value, dict)
                and isinstance(final_value, dict)
            ):
                self.__write_modified_values(
                    filewriter, product_id, off_value, fdc_value, final_value, full_key
                )

            elif off_value != final_value and full_key not in [
                "_id",
                "fdc_id",
                "modified_date",
                "data_source",
                "id_original",
                "fdc_category_en",
            ]:
                line = [product_id, full_key, off_value, final_value, fdc_value]
                filewriter.writerow(line)

    def create_csv_modification_report_for_field(
        self, field_name, analyze_empty_fields=True, use_docker=True
    ):
        parent_dir, off_cursor, fdc_cursor, final_cursor = self.__get_products(
            use_docker
        )

        off_product = next(off_cursor, None)
        fdc_product = next(fdc_cursor, None)
        final_product = next(final_cursor, None)

        csv_file = os.path.join(parent_dir, "data", f"modifications_{field_name}.csv")
        logging.info(f"Creating csv file: {csv_file}")
        with open(csv_file, "w", encoding="utf-8", newline="") as file:
            filewriter = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            columns = ["id", "value_off", "value_final", "value_fdc"]
            filewriter.writerow(columns)
            nb_products = 0
            wanted_field = field_name.split(".")

            while off_product and fdc_product and final_product:
                off_value = off_product
                fdc_value = fdc_product
                final_value = final_product

                for field in wanted_field:
                    off_value = off_value.get(field)
                    fdc_value = fdc_value.get(field)
                    final_value = final_value.get(field)

                if off_value != final_value and (
                    analyze_empty_fields
                    or (off_value is not None and fdc_value is not None)
                ):
                    line = [
                        off_product.get("id_match"),
                        off_value,
                        final_value,
                        fdc_value,
                    ]
                    filewriter.writerow(line)
                    nb_products += 1

                if nb_products >= 2000:
                    break

                off_product = next(off_cursor, None)
                fdc_product = next(fdc_cursor, None)
                final_product = next(final_cursor, None)

            logging.info("Csv file created!")

    @staticmethod
    def __get_products(use_docker=True):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)

        connection_string = (
            "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
        )

        client = MongoClient(connection_string)
        db = client["openfoodfacts"]

        matched_off_products = db["matched_off_products"].find().sort("id_match", 1)
        matched_fdc_products = db["matched_fdc_products"].find().sort("id_match", 1)
        final_products = db["final_products"].find().sort("id_match", 1)

        off_cursor = iter(matched_off_products)
        fdc_cursor = iter(matched_fdc_products)
        final_cursor = iter(final_products)

        return parent_dir, off_cursor, fdc_cursor, final_cursor
