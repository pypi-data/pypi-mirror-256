import numpy as np
from typing import Optional
from numba import njit, float32, int64, types, prange


@njit([(float32[:], int64),
      (float32[:], types.misc.Omitted(value=1))])
def rotational_direction(data: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Jitted compute of frame-by-frame rotational direction within a 1D timeseries array of angular data.

    :parameter ndarray data: 1D array of size len(frames) representing degrees.
    :return numpy.ndarray: An array of directional indicators.
       - 0 indicates no rotational change relative to prior frame.
       - 1 indicates a clockwise rotational change relative to prior frame.
       - 2 indicates a counter-clockwise rotational change relative to prior frame.

    .. note::
       * For the first frame, no rotation is possible so is populated with -1.
       * Frame-by-frame rotations of 180° degrees are denoted as clockwise rotations.

    .. image:: _static/img/rotational_direction.png
       :width: 600
       :align: center

    :example:
    >>> data = np.array([45, 50, 35, 50, 80, 350, 350, 0 , 180]).astype(np.float32)
    >>> CircularStatisticsMixin().rotational_direction(data)
    >>> [-1.,  1.,  2.,  1.,  1.,  2.,  0.,  1.,  1.]
    """

    data = data % 360
    data = np.deg2rad(data)
    result, prior_idx = np.full((data.shape[0]), -1.0), 0
    for i in prange(int(stride), data.shape[0]):
        prior_angle = data[prior_idx]
        current_angle = data[i]
        angle_diff = current_angle - prior_angle

        if angle_diff > np.pi:
            angle_diff -= 2 * np.pi
        elif angle_diff < -np.pi:
            angle_diff += 2 * np.pi

        if angle_diff == 0:
            result[i] = 0
        elif angle_diff > 0:
            result[i] = 1
        else:
            result[i] = 2
        prior_idx += 1
    return result.astype(np.int8)

data = np.array([0, 45, 90, 45], dtype=np.float32)
x = rotational_direction(data=data, stride=2)




