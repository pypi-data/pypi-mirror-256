from demand_model.base import BaseModelPredictor
from datetime import date, timedelta
from typing import Any, Optional, Union, Iterable
import pandas as pd

from demand_model.stock_and_flow.transitions import transition_population
from demand_model.base import combine_rates
try:
    import tqdm
except ImportError:
    tqdm = None


class StockAndFlowPredictor(BaseModelPredictor):
    def __init__(
        self,
        population: pd.Series,
        transition_rates: Optional[pd.Series] = None,
        transition_numbers: Optional[pd.Series] = None,
        start_date: date = date.today(),
        rate_adjustment: Union[pd.Series, Iterable[pd.Series]] = None,
        number_adjustment: Union[pd.Series, Iterable[pd.Series]] = None,
        external_bin_identifier: Optional[Any] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
  
        if transition_numbers is not None:
            transition_numbers.index.names = ["from", "to"]
            if number_adjustment is not None:
                if isinstance(number_adjustment, pd.Series):
                    number_adjustment = [number_adjustment]
                for adjustment in number_adjustment:
                    adjustment = adjustment.copy()
                    adjustment.index.names = ["from", "to"]
                    transition_numbers = combine_rates(transition_numbers, adjustment)

        if transition_rates is not None:
            transition_rates.index.names = ["from", "to"]
            if rate_adjustment is not None:
                if isinstance(rate_adjustment, pd.Series):
                    rate_adjustment = [rate_adjustment]
                for adjustment in rate_adjustment:
                    adjustment = adjustment.copy()
                    adjustment.index.names = ["from", "to"]
                    transition_rates = combine_rates(transition_rates, adjustment)

        self._initial_population = population
        self._transition_rates = transition_rates
        self._transition_numbers = transition_numbers
        self._start_date = start_date
        self._external_bin_identifier = external_bin_identifier

    @property
    def transition_rates(self):
        if self._transition_rates is not None:
            return self._transition_rates.copy()
        return None

    @property
    def transition_numbers(self):
        if self._transition_numbers is not None:
            return self._transition_numbers.copy()
        return None

    @property
    def initial_population(self):
        return self._initial_population

    @property
    def date(self):
        return self._start_date

    @property
    def external_bin_identifier(self):
        return self._external_bin_identifier

    def next(self, step_days: int = 1) -> "StockAndFlowPredictor":
        next_population = transition_population(
            self.initial_population,
            self.transition_rates,
            self.transition_numbers,
            days=step_days,
            external_bin_identifier=self.external_bin_identifier,
        )

        next_date = self.date + timedelta(days=step_days)
        next_population.name = next_date

        return StockAndFlowPredictor(
            population=next_population,
            transition_rates=self.transition_rates,
            transition_numbers=self.transition_numbers,
            start_date=next_date,
            external_bin_identifier=self.external_bin_identifier,
        )

    def predict(self, steps: int = 1, step_days: int = 1, progress=False) -> pd.DataFrame:
        predictor = self

        if progress and tqdm:
            iterator = tqdm.trange(steps)
            set_description = iterator.set_description
        else:
            iterator = range(steps)
            set_description = lambda x: None

        predictions = []
        for i in iterator:
            predictor = predictor.next(step_days=step_days)

            pop = predictor.initial_population
            pop.name = self.date + timedelta(days=(i + 1) * step_days)
            predictions.append(pop)

            set_description(f"{pop.name:%Y-%m}")
        return pd.concat(predictions, axis=1).T

    