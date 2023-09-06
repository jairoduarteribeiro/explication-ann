import logging

from pathlib import Path

from src.datasets.utils import is_dataset_prepared, prepare_and_save_dataset, read_all_datasets
from src.models.utils import train

if __name__ == '__main__':
    Path('log').mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log/app.log',
        filemode='w',
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    dataset_name = 'iris'
    if not is_dataset_prepared(dataset_name):
        logging.info(f'Preparing the dataset {dataset_name}...')
        prepare_and_save_dataset(dataset_name)
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = read_all_datasets(dataset_name)
    train(dataset_name, x_train, y_train, x_val, y_val, x_test, y_test)
