import logging

from pymongo import MongoClient

from domain.product.product import Product


class DataLoader:
    @staticmethod
    def load_products_to_mongo(
        products: list[Product],
        db_name: str = "openfoodfacts",
        collection_name: str = "products",
        use_docker: bool = True,
    ) -> None:
        try:
            logging.info("Loading products to MongoDB...")

            # Connect to MongoDB
            connection_string = "localhost:37017"
            client = MongoClient(connection_string)
            db = client[db_name]
            collection = db[collection_name]

            logging.info("Connected to client")

            # Check if the collection already contains data
            if collection.estimated_document_count() > 0:
                logging.info(
                    f"MongoDB collection {collection_name} already contains data. Skipping import."
                )
                return

            # Insert products into MongoDB
            logging.info("Inserting data into MongoDB...")
            BATCH_SIZE = 5000

            for i in range(0, len(products), BATCH_SIZE):
                batch = products[i : i + BATCH_SIZE]
                collection.insert_many([product.model_dump() for product in batch])
                logging.info(f"Inserted batch {i//BATCH_SIZE + 1}")

            logging.info(f"Data loading complete into {db_name}.{collection_name}")

            # collection.insert_many([product.model_dump() for product in products])
            # logging.info(f"Data loading complete into {db_name}.{collection_name}")

        except Exception as e:
            logging.info(
                f"Problem while loading the products in {db_name}.{collection_name}: {e}"
            )
