import logging
import tensorflow as tf
import platform

from os.path import dirname, exists, join
from time import time

from src.models.digits import digits
from src.models.iris import iris
from src.models.mnist import mnist
from src.models.sonar import sonar
from src.models.wine import wine


def _get_model_path(*paths):
    return join(dirname(__file__), *paths)


def _get_params_factory(dataset_name):
    if dataset_name == 'digits':
        return digits.get_params()
    elif dataset_name == 'iris':
        return iris.get_params()
    elif dataset_name == 'mnist':
        return mnist.get_params()
    elif dataset_name == 'sonar':
        return sonar.get_params()
    elif dataset_name == 'wine':
        return wine.get_params()


def is_model_trained(dataset_name):
    if exists(_get_model_path(dataset_name, f'{dataset_name}.h5')):
        logging.info(f'Model of {dataset_name} is already trained.')
        return True
    return False


def load_model(dataset_name) -> tf.keras.models.Sequential:
    model_path = _get_model_path(dataset_name, f'{dataset_name}.h5')
    return tf.keras.models.load_model(model_path)


def evaluate(model: tf.keras.models.Sequential, x_test, y_test):
    dataset_name = model.name
    batch_size = _get_params_factory(dataset_name)['batch_size']
    logging.info(f'Starting to evaluate the dataset {dataset_name}...')
    start_time = time()
    loss, accuracy = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=0)
    logging.info(f'Result of evaluation:\n- Loss: {loss}\n- Accuracy: {accuracy * 100:.2f}%')
    logging.info(f'Time of evaluation: {time() - start_time:.4f} seconds.')


def train(dataset_name, x_train, y_train, x_val, y_val) -> tf.keras.models.Sequential:
    input_shape = (x_train.shape[1],)
    params = _get_params_factory(dataset_name)
    n_layers = params['n_layers']
    n_neurons = params['n_neurons']
    n_epochs = params['n_epochs']
    n_classes = params['n_classes']
    batch_size = params['batch_size']
    model = tf.keras.models.Sequential(name=dataset_name)
    model.add(tf.keras.layers.Dense(n_neurons, input_shape=input_shape, activation=tf.keras.activations.relu))
    for _ in range(n_layers - 2):
        model.add(tf.keras.layers.Dense(n_neurons, activation=tf.keras.activations.relu))
    model.add(tf.keras.layers.Dense(n_classes, activation=tf.keras.activations.softmax))
    optimizer = tf.keras.optimizers.legacy.Adam() if platform.system() == 'Darwin' \
        else tf.keras.optimizers.Adam()
    loss = tf.keras.losses.SparseCategoricalCrossentropy()
    metrics = (tf.keras.metrics.SparseCategoricalAccuracy(),)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    patience = int(n_epochs * 0.1)
    filepath = _get_model_path(dataset_name, f'{dataset_name}.h5')
    callbacks = (
        tf.keras.callbacks.EarlyStopping(patience=patience),
        tf.keras.callbacks.ModelCheckpoint(filepath=filepath, save_best_only=True)
    )
    logging.info(f'Starting to train the dataset {dataset_name}...')
    start_time = time()
    model.fit(
        x_train,
        y_train,
        epochs=n_epochs,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        callbacks=callbacks,
        verbose=0
    )
    logging.info(f'Time of training: {time() - start_time:.4f} seconds.')
    return model
