import gzip
import logging
import os
import zipfile

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


class DataDownloader:
    def download_and_decompress_data(
        self,
        source_url: str,
        compressed_file: str,
        compressed_file_extension: str,
        decompressed_file: str,
    ) -> None:
        """Downloads and decompresses the file at a given url
        Args:
            source_url: the url to download the file from
            compressed_file: the path to the downloaded compressed file
            compressed_file_extension: the extension of the downloaded compressed file
            decompressed_file: the path to the decompressed file"""
        if os.path.exists(decompressed_file):
            logging.info(f"File {decompressed_file} already exists. Skipping download.")
            return

        self.__download_file(source_url, compressed_file)
        self.__decompress_file(
            compressed_file, compressed_file_extension, decompressed_file
        )

    @staticmethod
    def __download_file(
        url: str,
        download_path: str,
        chunk_size: int = 1024 * 1024,
        max_retries: int = 5,
        timeout: int = 60,
    ) -> None:
        """Downloads a file from a given url into a given download path"""
        logging.info(f"Downloading file from {url}...")

        @retry(stop=stop_after_attempt(max_retries), wait=wait_fixed(5))
        def download():
            try:
                with requests.get(url, stream=True, timeout=timeout) as response:
                    response.raise_for_status()
                    with open(download_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            f.write(chunk)
                logging.info(f"Download complete: {download_path}")
            except requests.exceptions.RequestException as exc:
                logging.error(f"Error downloading file {exc}")
                raise

        try:
            download()
        except Exception as e:
            logging.error(f"Download failed after {max_retries} attempts: {e}")
            raise

    def __decompress_file(
        self,
        compressed_file: str,
        compressed_file_extension: str,
        output_file: str,
        buffer_size: int = 1024 * 1024,
    ) -> None:
        """Decompresses a given file into a file named output_file"""
        logging.info(f"Decompressing {compressed_file} into {output_file}...")

        if compressed_file_extension == ".gz":
            self.__decompress_gz_file(compressed_file, output_file, buffer_size)
        elif compressed_file_extension == ".zip":
            self.__decompress_zip_file(compressed_file, output_file, buffer_size)
        else:
            logging.error(f"Unsupported file extension: {compressed_file_extension}")
            raise ValueError(
                f"Unsupported file extension: {compressed_file_extension}. Supported extensions are '.gz' and '.zip'."
            )
        logging.info("Decompression complete")

    @staticmethod
    def __decompress_gz_file(
        gz_file: str, output_file: str, buffer_size: int = 1024 * 1024
    ) -> None:
        """Decompresses a .gz file into a file named output_file"""
        with gzip.open(gz_file, "rb") as f_in:
            with open(output_file, "wb") as f_out:
                while chunk := f_in.read(buffer_size):
                    f_out.write(chunk)

    @staticmethod
    def __decompress_zip_file(
        zip_file: str, output_file: str, buffer_size: int = 1024 * 1024
    ) -> None:
        """Decompresses a .zip file into a file named output_file"""
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            with zip_ref.open(zip_ref.namelist()[0], "r") as f_in:
                with open(output_file, "wb") as f_out:
                    while chunk := f_in.read(buffer_size):
                        f_out.write(chunk)
