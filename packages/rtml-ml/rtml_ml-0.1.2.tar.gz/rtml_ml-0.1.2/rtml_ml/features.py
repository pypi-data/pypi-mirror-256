from typing import Optional

import pandas as pd
import talib

def add_momentum_indicators(
    ts_data: pd.DataFrame,
    # window_size=5
) -> pd.DataFrame:
    
    ts_data['RSI'] = talib.RSI(ts_data['close'], timeperiod=14)

    # Calculate MACD (Moving Average Convergence Divergence)
    macd, macd_signal, _ = talib.MACD(ts_data['close'],
                                      fastperiod=12,
                                      slowperiod=26,
                                      signalperiod=9)
    ts_data['MACD'] = macd
    ts_data['MACD_Signal'] = macd_signal

    # Calculate Momentum
    ts_data['Momentum'] = talib.MOM(ts_data['close'], timeperiod=10)

    return ts_data

def add_volatility_indicators(
    ts_data: pd.DataFrame,
    # window_size=5
) -> pd.DataFrame:
    
    # Calculate ATR (Average True Range)
    ts_data['ATR'] = talib.ATR(ts_data['high'], ts_data['low'], ts_data['close'], timeperiod=14)

    # # Calculate Bollinger Bands
    # upper_band, middle_band, lower_band = talib.BBANDS(ts_data['close'], timeperiod=20)
    # ts_data['BB_Upper'] = upper_band
    # ts_data['BB_Middle'] = middle_band
    # ts_data['BB_Lower'] = lower_band

    ts_data['STD'] = talib.STDDEV(ts_data['close'], timeperiod=20)

    return ts_data

def add_last_observed_target(
    ts_data: pd.DataFrame,
    window_size: Optional[int] = 1,
) -> pd.DataFrame:
    
    ts_data['last_observed_target'] = ts_data['target'].shift(window_size)
    
    return ts_data