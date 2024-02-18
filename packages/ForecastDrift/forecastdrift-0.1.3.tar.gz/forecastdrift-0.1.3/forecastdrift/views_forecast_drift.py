from sklearn import metrics
from views_forecasts.extensions import *
from dataclasses import dataclass
import warnings
import numpy as np
from . import alarm

@dataclass
class ForecastTable:
    """
    A dataclass to hold the forecast table with some simple metadata
    So that we don't eat our tail and circular call the extensions recursively
    """
    run_id: int
    run_name: str
    model_name: str
    model_df: pd.DataFrame

class ForecastDrift:
    """
    A class to detect drift in forecast scores tailored for Views use
    """
    def __init__(self,
                 forecasts: List[ForecastTable],
                 model_name: str,
                 verbose: bool = True):
        """
        :param forecasts: A list of ForecastTable objects
        :param model_name: The name of the model you're using, e.g. sleeping_unicorn
        :param verbose: Print warnings or not
        """

        if verbose:
            self.__warn = warnings.warn
        else:
            self.__warn = lambda *args, **kwargs: None

        self.forecasts = forecasts
        self.model_name = model_name.strip().lower()
        self.score = None

    @classmethod
    def from_store(cls, run_base_name: str, model_name: str, max_tail=12, verbose = True):
        """
        A factory method to create a ForecastDrift object from the VIEWS prediction store.
        :param run_base_name: Base name of the run that is to be used for the drift detection. Example: "forecasts_004"
        :param model_name: Model name, e.g. "slumbering_dragon"
        :return: A ForecastDrift object
        """

        runs = ViewsMetadata().get_runs_by_name(name=run_base_name.strip().lower(),
                                                     strict=False).tail(max_tail)
        if runs.shape[0] == 0:
            raise ValueError(f"No base run exists!")
        if runs.shape[0] < 2:
            raise ValueError(f"Need at least two runs to compare for drift detection!")

        stored_factory = cls(forecasts=[], model_name=model_name, verbose=verbose)
        stored_factory.__fetch_forecasts(runs=runs)
        return stored_factory


    def __fetch_forecasts(self, runs):
        """
        Fetches forecasts from the prediction store and puts them into a list of ForecastTable objects.
        :return: a list of ForecastTable objects.
        """
        collector = []

        for row in runs.iterrows():
            try:
                collector += [ForecastTable(
                    run_id=row[0],
                    run_name=row[1][0],
                    model_name=self.model_name,
                    model_df=pd.DataFrame.forecasts.read_store(run=row[0], name=self.model_name)
                )]
            except KeyError:
                self.__warn(f"Model {self.model_name} does not exist for run {row[1][0]}! Skipping...")
                if runs.index.max() == row[0]:
                    # Escalate to error if the last run is missing
                    raise ValueError(f"Model not available in newest in Views Storage. No drift detection possible!")

        if len(collector) < 2:
            raise ValueError(f"Need at least two forecasts to compare for drift detection! Less than two available!")

        self.forecasts = collector

    def single_drift(self,
                       metric: metrics,
                       actual_column: str,
                       forecast_column: str,
                       threshold: float = 0.05):
        """
        Detects drift between the last two prediction score tables.
        :param metric: Scikit-learn metric object
        :param actual_column: Name of the column containing the actuals
        :param forecast_column: Name of the column containing the forecasted values
        :param threshold: A threshold, in absolute terms for drift detection alarms
        :return: An Alarm object
        """

        score = []
        for forecast in self.forecasts[-2:]:
            actuals = forecast.model_df[actual_column]
            forecast = forecast.model_df[forecast_column]
            score += [metric(actuals, forecast)]

        self.score = score

        if (np.abs(score[1] - score[0]))/(score[1]+1e-100) > threshold:
            return alarm.Alarm(
                message=f"Drift detected in {forecast_column}! Score difference: {score[1] - score[0]}",
                severity=1
            )
        else:
            return None

    def ts_drift(self,
                      metric: metrics,
                      actual_column: str,
                      forecast_column: str,
                      avg_func: np.ufunc = np.mean,
                      disp_func: np.ufunc = np.std,
                      sigma_threshold: float = 1.96,
                      ar:int = 12):
        """
        Detects drift between the last prediction score table and the rest of the tables.
        :param metric: Scikit-learn metric object
        :param actual_column: Name of the column containing the actuals.
        :param forecast_column: Name of the column containing the forecasted values
        :param sigma_threshold: Standard deviation threshold at which alarm is sounded
        :return: An Alarm object
        """

        if len(self.forecasts) < 2:
            raise ValueError(f"Need at least three forecasts to compare for time-series drift detection!")

        score = []
        for forecast in self.forecasts:
            actuals = forecast.model_df[actual_column]
            forecast = forecast.model_df[forecast_column]
            score += [metric(actuals, forecast)]

        self.score = score

        old_score_avg = avg_func(np.array(score)[-ar:-1])
        old_score_sd = disp_func(np.array(score)[-ar:-1])
        new_score = score[-1]

        low = old_score_avg - sigma_threshold*old_score_sd
        high = old_score_avg + sigma_threshold*old_score_sd
        if not(low < new_score < high):
            return alarm.Alarm(
                message=f"Drift detected in {forecast_column}! Expected score is {old_score_avg} (CI: {low - high}. "
                        f"Received: {new_score}",
                severity=2
            )
        else:
            return None