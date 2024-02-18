from numba import njit, prange, int64, float32, types
import numpy as np
from numba.typed import Dict, List
from typing import Optional



# @njit("(float32[:], int64, int64,)", fastmath=True)
@njit([(float32[:], int64, int64),
       (float32[:], types.misc.Omitted(value=3), int64),
       (float32[:], int64, types.misc.Omitted(value=1)),
       (float32[:], types.misc.O(value=3), types.misc.Omitted(value=1))])
def permutation_entropy(data: np.ndarray,
                        dimension: Optional[int] = 3,
                        delay: Optional[int] = 1) -> float:
    """
    Calculate the permutation entropy of a time series.

    Permutation entropy is a measure of the complexity of a time series data by quantifying
    the irregularity and unpredictability of its order patterns. It is computed based on the
    frequency of unique order patterns of a given dimension in the time series data.

    The permutation entropy (PE) is calculated using the following formula:

    .. math::
        PE = - \\sum(p_i \\log(p_i))

    where:
    - PE is the permutation entropy.
    - p_i is the probability of each unique order pattern.

    :param numpy.ndarray data: The time series data for which permutation entropy is calculated.
    :param int dimension: It specifies the length of the order patterns to be considered.
    :param int delay: Time delay between elements in an order pattern.
    :return float: The permutation entropy of the time series, indicating its complexity and predictability. A higher permutation entropy value indicates higher complexity and unpredictability in the time series.

    :example:
    >>> t = np.linspace(0, 50, int(44100 * 2.0), endpoint=False)
    >>> sine_wave = 1.0 * np.sin(2 * np.pi * 1.0 * t).astype(np.float32)
    >>> TimeseriesFeatureMixin().permutation_entropy(data=sine_wave, dimension=3, delay=1)
    >>> 0.701970058666407
    >>> np.random.shuffle(sine_wave)
    >>> TimeseriesFeatureMixin().permutation_entropy(data=sine_wave, dimension=3, delay=1)
    >>> 1.79172449934604
    """

    n, permutations, counts = len(data), List(), List()
    for i in prange(n - (dimension - 1) * delay):
        indices = np.arange(i, i + dimension * delay, delay)
        permutation = List(np.argsort(data[indices]))
        is_unique = True
        for j in range(len(permutations)):
            p = permutations[j]
            if len(p) == len(permutation):
                is_equal = True
                for k in range(len(p)):
                    if p[k] != permutation[k]:
                        is_equal = False
                        break
                if is_equal:
                    is_unique = False
                    counts[j] += 1
                    break
        if is_unique:
            permutations.append(permutation)
            counts.append(1)

    total_permutations = len(permutations)
    probs = np.empty(total_permutations, dtype=types.float64)
    for i in prange(total_permutations):
        probs[i] = counts[i] / (n - (dimension - 1) * delay)

    return -np.sum(probs * np.log(probs))


data = np.arange(0, 1000, 2).astype(np.float32)
permutation_entropy(data=data)