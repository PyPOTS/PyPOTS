"""
The implementation of linear interpolation for the partially-observed time-series imputation task.
"""

# Created by Cole Sussmeier <colesussmeier@gmail.com>
# License: BSD-3-Clause

import warnings
from typing import Union, Optional

import h5py
import numpy as np
import torch

from ..base import BaseImputer


class Lerp(BaseImputer):
    """Linear interpolation (Lerp) imputation method.

    Lerp will linearly interpolate missing values between the nearest non-missing values.
    If there are missing values at the beginning or end of the series, they will be back-filled or
    forward-filled with the nearest non-missing value, respectively.
    If an entire series is empty, all 'nan' values will be filled with zeros.
    """

    def __init__(
        self,
    ):
        super().__init__()

    def fit(
        self,
        train_set: Union[dict, str],
        val_set: Optional[Union[dict, str]] = None,
        file_type: str = "hdf5",
    ) -> None:
        """Train the imputer on the given data.

        Warnings
        --------
        Linear interpolation class does not need to run fit().
        Please run func ``predict()`` directly.
        """
        warnings.warn(
            "Linear interpolation class has no parameter to train. "
            "Please run func `predict()` directly."
        )

    def predict(
        self,
        test_set: Union[dict, str],
        file_type: str = "hdf5",
    ) -> dict:
        """Make predictions for the input data with the trained model.

        Parameters
        ----------
        test_set : dict or str
            The dataset for model validating, should be a dictionary including keys as 'X',
            or a path string locating a data file supported by PyPOTS (e.g. h5 file).
            If it is a dict, X should be array-like of shape [n_samples, sequence length (n_steps), n_features],
            which is time-series data for validating, can contain missing values, and y should be array-like of shape
            [n_samples], which is classification labels of X.
            If it is a path string, the path should point to a data file, e.g. a h5 file, which contains
            key-value pairs like a dict, and it has to include keys as 'X' and 'y'.

        file_type :
            The type of the given file if test_set is a path string.

        Returns
        -------
        result_dict: dict
            Prediction results in a Python Dictionary for the given samples.
            It should be a dictionary including keys as 'imputation', 'classification', 'clustering', and 'forecasting'.
            For sure, only the keys that relevant tasks are supported by the model will be returned.
        """
        if isinstance(test_set, str):
            with h5py.File(test_set, "r") as f:
                X = f["X"][:]
        else:
            X = test_set["X"]

        assert len(X.shape) == 3, (
            f"Input X should have 3 dimensions [n_samples, n_steps, n_features], "
            f"but the actual shape of X: {X.shape}"
        )
        if isinstance(X, list):
            X = np.asarray(X)

        def _interpolate_missing_values(X: np.ndarray):
            nans = np.isnan(X)
            nan_index = np.where(nans)[0]
            index = np.where(~nans)[0]
            if np.any(nans) and index.size > 1:
                X[nans] = np.interp(nan_index, index, X[~nans])
            elif np.any(nans):
                X[nans] = 0

        if isinstance(X, np.ndarray):

            trans_X = X.transpose((0, 2, 1))
            n_samples, n_features, n_steps = trans_X.shape
            reshaped_X = np.reshape(trans_X, (-1, n_steps))
            imputed_X = np.ones(reshaped_X.shape)

            for i, univariate_series in enumerate(reshaped_X):
                t = np.copy(univariate_series)
                _interpolate_missing_values(t)
                imputed_X[i] = t

            imputed_trans_X = np.reshape(imputed_X, (n_samples, n_features, -1))
            imputed_data = imputed_trans_X.transpose((0, 2, 1))

        elif isinstance(X, torch.Tensor):

            trans_X = X.permute(0, 2, 1)
            n_samples, n_features, n_steps = trans_X.shape
            reshaped_X = trans_X.reshape(-1, n_steps)
            imputed_X = torch.ones_like(reshaped_X)

            for i, univariate_series in enumerate(reshaped_X):
                t = univariate_series.clone().cpu().detach().numpy()
                _interpolate_missing_values(t)
                imputed_X[i] = torch.from_numpy(t)

            imputed_trans_X = imputed_X.reshape(n_samples, n_features, -1)
            imputed_data = imputed_trans_X.permute(0, 2, 1)

        else:
            raise ValueError()

        result_dict = {
            "imputation": imputed_data,
        }
        return result_dict

    def impute(
        self,
        test_set: Union[dict, str],
        file_type: str = "hdf5",
    ) -> np.ndarray:
        """Impute missing values in the given data with the trained model.

        Parameters
        ----------
        test_set :
            The data samples for testing, should be array-like of shape [n_samples, sequence length (n_steps),
            n_features], or a path string locating a data file, e.g. h5 file.

        file_type :
            The type of the given file if X is a path string.

        Returns
        -------
        array-like, shape [n_samples, sequence length (n_steps), n_features],
            Imputed data.
        """

        result_dict = self.predict(test_set, file_type=file_type)
        return result_dict["imputation"]
