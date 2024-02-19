"""
This module contains the implementation of the
FR Test Statistic based estimate and the
FNN based estimate for the Bayes Error Rate

Learning to Bound the Multi-class Bayes Error (Th. 3 and Th. 4)
https://arxiv.org/abs/1811.06419
"""

from abc import abstractmethod
from typing import Tuple

import numpy as np
from scipy.sparse import coo_matrix

from daml._internal.metrics.aria.base import _BaseMetric
from daml._internal.metrics.outputs import BEROutput

from .utils import compute_neighbors, get_classes_counts, minimum_spanning_tree


class _MultiClassBer(_BaseMetric):
    def __init__(self, data: np.ndarray, labels: np.ndarray) -> None:
        self.data = data
        self.labels = labels

    @abstractmethod
    def _multiclass_ber(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Abstract method for the implementation of multiclass BER calculation"""

    def evaluate(self) -> BEROutput:
        """
        Calculates the Bayes Error Rate estimate

        Returns
        -------
        BEROutput
            The estimated upper and lower bounds of the Bayes Error Rate

        Raises
        ------
        ValueError
            If unique classes M < 2
        """
        # Pass X through an autoencoder before evaluating BER
        ber, ber_lower = self._multiclass_ber(self.data, self.labels)
        return BEROutput(ber=ber, ber_lower=ber_lower)


class MultiClassBerMST(_MultiClassBer):
    """
    An FR test statistic based estimator for Multi-class Bayes Error Rate

    Parameters
    ----------
    data : np.ndarray
        Array of images or image embeddings
    labels : np.ndarray
        Array of labels for each image or image embedding

    See Also
    --------
    `Learning to Bound the Multi-class Bayes Error (Th. 3 and Th. 4) <https://arxiv.org/abs/1811.06419>`_
    """  # noqa F401

    def _multiclass_ber(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        M, N = get_classes_counts(y)

        tree = coo_matrix(minimum_spanning_tree(X))
        matches = np.sum([y[tree.row[i]] != y[tree.col[i]] for i in range(N - 1)])
        deltas = matches / (2 * N)
        upper = 2 * deltas
        lower = ((M - 1) / (M)) * (1 - (1 - 2 * ((M) / (M - 1)) * deltas) ** 0.5)
        return upper, lower


class MultiClassBerFNN(_MultiClassBer):
    """
    A KNN test statistic based estimator for Multi-class Bayes Error Rate

    Parameters
    ----------
    data : np.ndarray
        Array of images or image embeddings
    labels : np.ndarray
        Array of labels for each image or image embedding

    See Also
    --------
    `Learning to Bound the Multi-class Bayes Error (Th. 3 and Th. 4) <https://arxiv.org/abs/1811.06419>`_
    """  # noqa F401

    def _multiclass_ber(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        M, N = get_classes_counts(y)

        # All features belong on second dimension
        X = X.reshape((X.shape[0], -1))
        nn_indices = compute_neighbors(X, X)
        deltas = float(np.count_nonzero(y[nn_indices] - y) / (2 * N))
        upper = 2 * deltas
        lower = ((M - 1) / (M)) * (1 - (1 - 2 * ((M) / (M - 1)) * deltas) ** 0.5)
        return upper, lower
