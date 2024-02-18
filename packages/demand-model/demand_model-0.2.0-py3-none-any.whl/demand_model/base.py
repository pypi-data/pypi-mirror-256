from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from dataclasses import dataclass
import pandas as pd



def combine_rates(rate1: pd.Series, rate2: pd.Series) -> pd.Series:
    rate1, rate2 = rate1.align(rate2, fill_value=0)
    rates = rate1 + rate2
    rates.index.names = ["from", "to"]
    return rates

class BaseModelPredictor(ABC):
    """
    This is the base class for all the prediction models.
    It should be used to implement the next and predict methods
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @abstractmethod
    def next(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self):
        raise NotImplementedError

