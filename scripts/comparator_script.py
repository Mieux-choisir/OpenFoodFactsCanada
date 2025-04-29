import logging

from scripts.product_completer import ProductCompleter


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    product_completer = ProductCompleter()

    product_completer.complete_products()


if __name__ == "__main__":
    main()
