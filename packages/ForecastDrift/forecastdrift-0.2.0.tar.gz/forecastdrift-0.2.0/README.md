# ForecastDrift

`ForecastDrift` is the MLOps drift detection and alerting system for the PRIO/UU VIEWS project. It is designed to monitor the drift of forecasts over time and alert the user when the drift exceeds a certain threshold. Supports drift detection against both one and multiple different prediction tables (time-series drift detection).

It can work with a user supplied lists of prediction tables or with the VIEWS Prediction Store, and can make use any of kind of machine learning metric, as well as of any kind of aggregation and dispersion function for time-series drift detection. Further, while it is design to work with the classical `viewser` type of predictions, it can also work with any kind of predictions, as long as they are supplied as Pandas dataframes.

## Installation

To install the package, simply run:

```pip install ForecastDrift``` in your dedicated `viewser` environment.

## Usage

`ForecastDrift` is designed to be used as a Python package. It can be used in two different ways:

1. As a standalone package, where the user supplies the prediction tables and the drift detection parameters.
2. As a part of the VIEWS Prediction Store, where the user supplies the drift detection parameters and the package automatically retrieves the prediction tables from the Prediction Store.

## Standalone package use

This will be the least common use case, as this should NEVER be used with models that are in the VIEWS pipeline. This is only for testing and development purposes of individual models as well as users that are not connected to VIEWS that want to use this code.

As a standalone package, the user can use the `ForecastDrift` class to monitor the drift of predictions that are stored locally, on the user's machine, over time. The user can supply a list of prediction tables, as well as the drift detection parameters, and the package will return a list of drift alerts, if any. To use `ForecastDrift` in this way you use the class constructor, and pass an **ORDERED** list of prediction tables, where the first table is the oldest and the last table is the most recent (i.e. the last table is the one for which drift detection is performed).

Note that you do not need to wrap you predictions in the `PredictionTable` class, you can just supply a list of DataFrames and it will wrap them for you. 

To use the ForecastDrift class in this way, you can use the following code:

```python
from ForecastDrift import ForecastDrift
drift = ForecastDrift(
    forecasts=[prediction_table_1, prediction_table_2, prediction_table_3, ...],
    model_name="my_model"
)
```

## Prediction store package use

This is the most common use case, as this is the way that the VIEWS pipeline is set up. This can be run manually, or as part of any script in the production pipeline or dev environment. 

As a part of the VIEWS Prediction Store, the user can use the `ForecastDrift` class to monitor the drift of predictions over time. The user can supply the drift detection parameters, and the package will automatically retrieve the prediction tables from the Prediction Store and return a list of drift alerts, if any (i.e. `None` if no alert is to be triggered). To use `ForecastDrift` in this way you use the factory method `ForecastDrift.from_prediction_store` to instantiate the class.

If used in this way, the user must have the necessary credentials to access the Prediction Store, i.e. the VIEWS certificates and the correct network authentication.

To use PredictionsStore in this way, you can use the following code:

```python
from ForecastDrift import ForecastDrift
drift = ForecastDrift.from_store(
    run_base_name="cabin",
    model_name="dragonizing_dragon",
    max_tail=12,
    verbose=False
)
```
Parameters here are important to get right:

- `run_base_name` follows the convention agreed for the Views Pipeline, being the name of the model set that you want to use, e.g. `cabin` or `fatalities_003` or `econ_001`. ONLY give the base name (e.g. `fatalities_003`), not the full run name of the latest name (e.g. `cabin_009_490_b`).

Comparisons will be made ACROSS runs, starting backwards from the current run, meaning, e.g., if t `fatalities_003_630_b` is the current run, the comparison will be made with `fatalities_003_630_a` `fatalities_003_629_a`, `fatalities_003_628_a`, etc. up to `fatalities_003_619_a` (in this case, 12 runs back).

Note that this means that you cannot use this mode to make drift detection for legacy runs, i.e. `fatalities_002` or older (`fatalities_001`, `escwa`, `d`, `r`, `demas` etc.) since they followed different conventions for how runs were organized, with multiple identical models belonging to different pipeline runs in the same run. 

- `model_name` is the name of the model that you want to use, e.g. `dragonizing_dragon`, `nuclear_narwal`, `enchanting_enchilada` or `zeroing_zebra`. This is the name of the model that you want to monitor the drift of. Note that you can monitor the drift of multiple columns from that model at the same time (e.g. multiple specifications) AND using multiple metrics, with the data being pulled only once, as long as you do not reiinstantiate the ForecastDrift class.

- `max_tail` is the maximum number of runs to look back. This is important to avoid pulling too much data from the Prediction Store, as it can be quite slow, given the PGM table is 15 million rows long. The default is 12, i.e. a year's worth of prediction but you can set it to any number you want that is higher or equal 2. Note that the number of runs that will be looked back is the minimum between `max_tail` and the number of runs available in the Prediction Store.

- `verbose` is a boolean that controls whether the class will print out information about the data it is pulling from the Prediction Store. The default is `False`.

# Drift detection.

There are two kinds of drift detection that can be performed with `ForecastDrift`: single prediction table drift detection and time-series drift detection.

## Single prediction table drift detection

```python
from sklearn.metrics import mean_absolute_error

drift.single_drift(metric=mean_absolute_error,
                   actual_column='ln_ged_sb_dep',
                   forecast_column='step_pred_1',
                   threshold=0.05)
```

This will perform drift detection for the `ln_ged_sb_dep` (actuals) and `step_pred_1` (forecast) column of the `dragonizing_dragon` model. The comparison will be done between the current run and the preceding run, using the `mean_absolute_error` metric, and a threshold of 0.05. The threshold is measured in relative drift of the metric, i.e. if the metric drifts more than 5% between runs, the method will return a drift alert (see below for specifications), otherwise it will return `None`.

If you want drift detection for other pairs of runs of the same model, you can reorder the `self.forecasts` list so that the models you want compared are the last two and call the method again.

Any metric that is available in the `sklearn.metrics` module can be used, as long as it is a function that takes two arrays of the same length and returns a single number. Note that multiclass drift detection cannot be performed with this method, as it only takes two columns as input, but you can achieve this using pairwise.

## Time-series drift detection

```python
import numpy as np
from sklearn.metrics import mean_absolute_error

alert = drift.ts_drift(metric=mean_absolute_error,
                        actual_column='ln_ged_sb_dep',
                        forecast_column='step_combined', 
                        sigma_threshold=1.96,
                        avg_func = np.mean,
                        disp_func = np.std,
                        ar = 12)
```

This will perform time-series drift detection for the `ln_ged_sb_dep` (actuals) and `step_combined` (forecast) column of the `dragonizing_dragon` model. The comparison will be done between the current run and EACH of the preceding number of runs loaded in the class (you can limit the number by specifying the `ar` parameter), using the `mean_absolute_error` metric.

The drift is computed between the value of the metric in the current run and the average of the metric in the preceding runs, and the alert is triggered if the drift exceeds the threshold, which is measured in standard deviations of the metric. The threshold is computed as the average of the metric in the preceding runs plus the threshold times the standard deviation of the metric in the preceding runs. The default threshold is 1.96, which corresponds to a 95% confidence interval.

Note that the averaging and dispersion function are customizable : while the mean (arithmetic) and standard deviations are the defaults, the `avg_func` and `disp_func` can be customized with whatever numpy function you want or need - e.g. a Bayesian distribution peak and mass density function -  as long as you can use any function that takes an array and returns a single number.

# Alert formats

The alerts are returned as objects of the `Alarm` class, which has the following attributes:

```python
self.message = message
self.severity = severity
self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

This class currently only contains these as attributes and `str` and `repr` magic methods, but it can be expanded to include more information about the alert, such as the model, the metric, the threshold, the actual value of the metric, the forecast value, etc. if needed through the conventional ways (inheritance etc.).

The `message` attribute is a string that contains the message of the alert, and the `severity` attribute is a numeric value which is currently set to 1 when triggered by the single prediction table drift detection and 2 when triggered by the time-series drift detection. 

The `timestamp` attribute is a string that contains the timestamp of the alert.

# Contact

For any questions, please contact the author of the package, Mihai Croicu.