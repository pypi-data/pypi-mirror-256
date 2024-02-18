from typing import Iterable
import pandas as pd


def process_transition_rates(transition_rates: pd.Series) -> pd.DataFrame:
    _transition_rates = populate_same_state_transition(transition_rates)
    return build_transition_rates_matrix(_transition_rates)



def populate_same_state_transition(transition_rates: pd.Series) -> pd.DataFrame:
    """
    Fill transition rates between the same states with 1 minus the sum of all the out rates.
    If the transition rate between the same state is not present, it will be added with the value of 1.
    """
    _transition_rates = transition_rates.copy()
    for value in _transition_rates.index.get_level_values(0).unique():
        total = _transition_rates.xs((value)).sum()
        try:
            current_value = _transition_rates.xs((value, value))
        except KeyError:
            current_value = 0
        _transition_rates.loc[(value, value)] = 1 - total + current_value
    return _transition_rates


def build_transition_rates_matrix(transition_rates: pd.Series) -> pd.DataFrame:
    """
    - Convert the transition rates to a matrix format, where the columns are the
      origin states and the index is the destination state. 
    - Ensure that the matrix is square by adding the missing states with a value of 1 and 0 for the rest.
    - Sort the matrix by the index and columns. 
    """
    matrix = transition_rates.unstack(0).fillna(0)
    for col in matrix.columns:
        if col not in matrix.index:
            new_row = pd.DataFrame([[0]*len(matrix.columns)], columns=matrix.columns, index=[col])
            new_row[col] = 1
            matrix = pd.concat([matrix, new_row]) 
    
    for idx in matrix.index:
        if idx not in matrix.columns:
            matrix[idx] = 0
            # tuples causes issues while updating a value in a dataframe with loc
            # so we need to get the integer locations of the index and columns
            ilocs = matrix.index.get_loc(idx), matrix.columns.get_loc(idx)
            matrix.iloc[ilocs] = 1

    return matrix.sort_index(axis=0).sort_index(axis=1)

def fill_missing_states(series: pd.Series, states: Iterable) -> pd.Series:
    """
    - Ensure that the series contain all the states in the "states" iterable.
    - Add the missing states with a value of 0.
    - Sort the rates by the index.
    """
    _series = series.copy()
    for idx in states:
        if idx not in _series.index:
            _series = pd.concat([_series, pd.Series(0, index=[idx])])
    return _series.sort_index()