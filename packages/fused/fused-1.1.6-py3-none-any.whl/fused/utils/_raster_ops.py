from typing import Any, Sequence

import numpy as np
import xarray as xr


def array_to_xarray(arr: Any, bbox: Sequence[float]) -> xr.DataArray:
    """
    Add a bounding box to a raster array.

    Args:
        arr: Data array, should either be a 2 dimensional array (for grayscale images) or 3 dimensional array (for color images, band first).
        bbox: Geographic bounds of the data, arranged as `min x, min y, max x, max y`.
    """

    if isinstance(arr, np.ndarray):
        if len(arr.shape) == 2:
            arr = xr.DataArray(arr, dims=["y", "x"])
        elif len(arr.shape) == 3:
            arr = xr.DataArray(arr, dims=["band", "y", "x"])
        else:
            raise ValueError(
                f"Invalid number of dimensions of arr: {len(arr.shape)}. Should be 2 (grayscale) or 3 (color)."
            )

    if isinstance(arr, xr.DataArray):
        arr.attrs["bounds"] = bbox
        return arr
    else:
        raise TypeError(
            f"Invalid input to array_to_xarray: {type(arr)}. Should be an xarray.DataArray or numpy.ndarray."
        )
