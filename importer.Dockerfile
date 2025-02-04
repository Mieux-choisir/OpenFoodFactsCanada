FROM python:3.10.15-bookworm

WORKDIR /

ENV DATA_PATH /data

# Download Open Food Facts data
RUN mkdir -p $DATA_PATH && \
    wget https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz \
    -O $DATA_PATH/en.openfoodfacts.org.products.csv && \
    gunzip $DATA_PATH/en.openfoodfacts.org.products.csv

# Download branded food data from USDA
RUN wget https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2024-10-31.zip \
    -O $DATA_PATH/FoodData_Central_json_2024-10-31.zip && \
    unzip $DATA_PATH/FoodData_Central_json_2024-10-31.zip -d $DATA_PATH

RUN apt-get update && apt-get install -y mdbtools

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "import.py"]
