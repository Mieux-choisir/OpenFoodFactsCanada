import logging
import concurrent.futures
from pymongo import MongoClient, UpdateOne, ASCENDING
from typing import List, Iterator
from domain.product.product import Product


class DataLoader:
    """
    This is a class that loads data into MongoDB.

    Methods:
        load_products_to_mongo(products, db_name, collection_name, use_docker, batch_size, max_workers): Loads given products into the MongoDB database
    """

    @staticmethod
    def load_products_to_mongo(
        products: List[Product] | Iterator[Product],
        db_name: str = "openfoodfacts",
        collection_name: str = "products",
        use_docker: bool = True,
        batch_size: int = 5000,
        max_workers: int = 5,
    ) -> None:
        """Loads given products into the MongoDB database"""
        try:
            logging.info(
                f"Loading products into MongoDB ({db_name}.{collection_name})..."
            )

            connection_string = (
                "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
            )

            client = MongoClient(connection_string)

            collection = client[db_name][collection_name]

            collection.create_index(
                [("id_match", ASCENDING), ("modified_date", ASCENDING)],
                unique=True,
                background=True,
            )
            logging.info("Connected to MongoDB, indexes created")

            def process_batch(batch):
                batch_client = MongoClient(connection_string)
                batch_collection = batch_client[db_name][collection_name]

                operations = {}
                for product in batch:
                    if not product.id_match:
                        continue

                    product_data = product.model_dump()
                    existing = operations.get(product.id_match)

                    if (
                        not existing
                        or product.publication_date > existing["modified_date"]
                    ):
                        operations[product.id_match] = product_data

                bulk_operations = [
                    UpdateOne(
                        {"id_match": data["id_match"]}, {"$set": data}, upsert=True
                    )
                    for data in operations.values()
                ]

                if bulk_operations:
                    batch_collection.bulk_write(bulk_operations, ordered=False)
                batch_client.close()

            batches = []
            current_batch = []

            for product in products:
                current_batch.append(product)
                if len(current_batch) >= batch_size:
                    batches.append(current_batch)
                    current_batch = []

            if current_batch:
                batches.append(current_batch)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(process_batch, batches)

            logging.info("Data loading complete")
            client.close()
        except Exception as e:
            logging.error(f"Error loading products in {db_name}.{collection_name}: {e}")
            raise

    @staticmethod
    def fetch_products_from_mongo(
        db_name: str = "openfoodfacts",
        collection_name: str = "fdc_products",
        use_docker: bool = True,
        product_ids: list[str] = None,
    ) -> list[Product]:
        """Fetches the products stored in the collection with the given name from the MongoDB database with the given name.
         If the list of product_ids has ids then only the products with the given ids are fetched from the collection.

         Args:
             db_name(str): The name of the MongoDB databse used to fetch products
             collection_name(str): The name of the MongoDB collection used to fetch products
             use_docker(bool): A boolean indicating whether to use docker
             product_ids(list[str]): A list of the ids of the wanted products, if empty, all products are fetched

        Returns:
            A list of the fetched products"""
        try:
            logging.info(
                f"Fetching products from MongoDB ({db_name}.{collection_name})..."
            )
            connection_string = (
                "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
            )
            client = MongoClient(connection_string)
            collection = client[db_name][collection_name]

            query = {}
            if product_ids is not None:
                query = {"id_match": {"$nin": product_ids}}

            raw_products = list(collection.find(query))

            products = [Product.from_dict(doc) for doc in raw_products]

            logging.info(f"Number of fetched products: {len(products)}")
            return products

        except Exception as e:
            logging.error("Error when fetching products: %s", e)
            return []
