from datetime import datetime, timedelta
import logging
from typing import Optional, Tuple
import os

from comet_ml import Experiment
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    classification_report,
)

from rtml_tools.logging import initialize_logger
from rtml_tools.config import YamlConfig
from rtml_ml.data import (
    get_ohlc_data_from_store,
    add_perc_change_column,
    get_perc_change_terciles,
    add_discrete_target_column
)
from rtml_ml.features import (
    add_momentum_indicators,
    add_volatility_indicators,
    add_last_observed_target,
)

initialize_logger()
logger = logging.getLogger()

# Load parameters from global config file
yaml_config = YamlConfig('../config.yml')
config = yaml_config._config['ml']


def split_train_test(
    ts_data: pd.DataFrame,
    train_test_cutoff_date: datetime,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the given `ts_data` by its `timestamp`
    using the provided `train_test_cutoff_date`.
    """
    train_test_cutoff_ms = int(train_test_cutoff_date.timestamp() * 1000)

    ts_train = ts_data[ts_data['timestamp'] < train_test_cutoff_ms]
    ts_test = ts_data[ts_data['timestamp'] >= train_test_cutoff_ms]
    return ts_train, ts_test

def train(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    train_test_cutoff_date: Optional[datetime] = None,
    product_id: Optional[str] = 'XBT/EUR',
    n_train_samples: Optional[int] = None,
):
    """
    - Gets OHLC data from the Feature store
    - Adds a target column
    - Trains a model
    - Saves the model in the model registry
    """
    experiment = Experiment(
        api_key=os.environ["COMET_API_KEY"],
        project_name=os.environ["COMET_PROJECT_NAME"],
        workspace=os.environ["COMET_WORKSPACE"],
    )

    if to_date is None:
        # to_date as current utc datetime rounded to the closest previous day
        to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    if from_date is None:
        # from_date as current utc datetime minus 90 days
        from_date = to_date - timedelta(days=90)

    if train_test_cutoff_date is None:
        # train_test_cutoff_date as current utc datetime minus 30 days
        train_test_cutoff_date = to_date - timedelta(days=30)

    experiment.log_parameters({
        "from_date": from_date,
        "to_date": to_date,
        "train_test_cutoff_date": train_test_cutoff_date,
        "product_id": product_id,
    })

    logger.info('Getting OHLC data from the Feature Store')
    ts_data = get_ohlc_data_from_store(
        from_date=from_date,
        to_date=to_date,
        product_id=product_id,
        cache_dir='../.cache/ohlc_data/'
    )
    experiment.log_dataset_hash(ts_data)
    
    logger.info('Splitting the data into training and test sets')
    ts_train, ts_test = split_train_test(ts_data, train_test_cutoff_date)

    if n_train_samples:
        logger.info(f'Picking a subset of {n_train_samples} samples to train the model')
        ts_train = ts_train.head(n_train_samples)

    logger.info('Add features to the training and test sets')    
    # momentum 
    ts_train = add_momentum_indicators(ts_train)
    ts_test = add_momentum_indicators(ts_test)
    # volatility
    ts_train = add_volatility_indicators(ts_train)
    ts_test = add_volatility_indicators(ts_test)

    logger.info('Adding percentage change column to training and test sets')
    ts_train = add_perc_change_column(ts_train,
                                      window_size=config['prediction_horizon_steps'],
                                      drop_nans=False)
    ts_test = add_perc_change_column(ts_test,
                                     window_size=config['prediction_horizon_steps'],
                                     drop_nans=False)

    logger.info('Computing terciles of percentage change using the training data')
    tercile_1, tercile_2 = get_perc_change_terciles(ts_train)
    experiment.log_parameter('target_terciles', [tercile_1, tercile_2])

    logger.info('Adding a discrete target column to the training and test sets')
    ts_train = add_discrete_target_column(ts_train, tercile_1, tercile_2)
    ts_test = add_discrete_target_column(ts_test, tercile_1, tercile_2)
    logger.info(f'Target distribution train data: \n {ts_train["target"].value_counts()}')
    logger.info(f'Target distribution test data: \n {ts_test["target"].value_counts()}')

    logger.info('Drop rows with NaN values from the training and test sets')
    ts_train = ts_train.dropna()
    ts_test = ts_test.dropna()

    logger.info('Split the training and test sets into features and target')
    features = config['features']
    # features = [
    #     # raw features
    #     'close',
    #     'volume',

    #     # momentum indicators
    #     'RSI',
    #     'MACD',
    #     'MACD_Signal',
    #     'Momentum',

    #     # volatility indicators
    #     'ATR',
    #     'STD',
    # ]
    X_train = ts_train[features]
    y_train = ts_train['target']
    X_test = ts_test[features]
    y_test = ts_test['target']
    logger.info(f'X_train.shape: {X_train.shape}')
    logger.info(f'y_train.shape: {y_train.shape}')
    logger.info(f'X_test.shape: {X_test.shape}')
    logger.info(f'y_test.shape: {y_test.shape}')
    experiment.log_parameter('features', features)

    logger.info('Train a model on the training data')
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    logger.info('Evaluate the model on the test data')
    y_pred = model.predict(X_test)
    
    # confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    logger.info("Confusion Matrix:")
    logger.info(conf_matrix)
    experiment.log_confusion_matrix(
        matrix=conf_matrix,
        labels=['-1', '0', '1']
    )
    
    # accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy:.2%}")
    experiment.log_metric('accuracy', accuracy)

    # classification report
    class_report = classification_report(y_test, y_pred)
    logger.info("Classification Report:")
    logger.info(class_report)
    experiment.log_text(class_report)

    # log the model
    # Save the model to a local file
    model_path = 'model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    # push the model to the comet.ml server
    model_name = f'{product_id.replace("/", "_")}_direction_predictor'
    logger.info(f"Logging the model to comet.ml as {model_name}")
    experiment.log_model(model_name, model_path)
    # register the model to the comet ML model registry
    experiment.register_model(model_name)
    # os.remove(model_path)
    
    logger.info('Model training and evaluation completed')

if __name__ == '__main__':

    # train(
    #     from_date=datetime(2023, 1, 6),
    #     to_date=datetime(2024, 2, 5),
    #     train_test_cutoff_date=datetime(2024, 1, 1),
    #     product_id='XBT/EUR',
    #     n_train_samples=100,
    # )
    from fire import Fire
    Fire(train)