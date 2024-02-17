import numpy as np

def sliding_circular_mean(data: np.ndarray, time_windows: np.ndarray, fps: int) -> np.ndarray:
    """
    Compute the circular mean in degrees within sliding temporal windows.

    :parameter np.ndarray data: 1d array with feature values in degrees.
    :parameter np.ndarray time_windows: Rolling time-windows as floats in seconds. E.g., [0.2, 0.4, 0.6]
    :parameter int fps: fps of the recorded video
    :returns np.ndarray: Size data.shape[0] x time_windows.shape[0] array

    .. image:: _static/img/mean_rolling_timeseries_angle.png
       :width: 600
       :align: center

    .. attention::
       The returned values represents the angular mean dispersion in the time-window ``[current_frame-time_window->current_frame]``.
       `-1` is returned when ``current_frame-time_window`` is less than 0.

    :example:
    >>> data = np.random.normal(loc=45, scale=1, size=20).astype(np.float32)
    >>> CircularStatisticsMixin().sliding_circular_mean(data=data,time_windows=np.array([0.5, 1.0]), fps=10)
    """

    data = np.deg2rad(data)
    results = np.full((data.shape[0], time_windows.shape[0]), -1.0)
    for time_window in range(time_windows.shape[0]):
        window_size = int(time_windows[time_window] * fps)
        for current_frm in range(window_size-1, results.shape[0]):
            data_window = data[(current_frm - window_size)+1: current_frm+1]
            m = np.rad2deg(np.arctan2(np.mean(np.sin(data_window)), np.mean(np.cos(data_window))))
            results[current_frm, time_window] = np.abs(np.round(m, 4))

    return results

data = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80]).astype(np.float32)


x = sliding_circular_mean(data=data, time_windows=np.array([1.0]), fps=3)

