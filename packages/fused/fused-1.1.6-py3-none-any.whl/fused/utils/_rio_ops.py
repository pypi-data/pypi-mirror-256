from __future__ import annotations

import numpy as np
import rasterio
import shapely
from affine import Affine
from scipy.ndimage import zoom

from ._impl._rio_ops_impl import rio_distance as _rio_distance

__all__ = (
    "rio_distance",
    "rio_resample",
    "rio_super_resolution",
    "rio_scale_shape_transform",
    "rio_geom_to_xy_slice",
)


def rio_distance(
    dataset,
    variable,
    suffix="_distance",
    coords_x="x",
    coords_y="y",
    chunk_size=500_000,
    verbose=False,
):
    return _rio_distance(
        dataset=dataset,
        variable=variable,
        suffix=suffix,
        coords_x=coords_x,
        coords_y=coords_y,
        chunk_size=chunk_size,
        verbose=verbose,
    )


def rio_resample(
    da1, da2, method="linear", reduce="mean", factor=None, order=1, verbose=True
):
    if da1.shape[0] >= da2.shape[0]:
        if not factor:
            factor = int(np.ceil(da1.shape[0] / da2.shape[0]))
        if verbose:
            print(f"downsampling: {reduce=}, {factor=}")
        return (
            da1.interp(
                x=zoom(da2.x, factor, order=order),
                y=zoom(da2.y, factor, order=order),
                method=method,
            )
            .coarsen(x=factor, y=factor)
            .reduce(reduce)
        )
    else:
        if verbose:
            print("upsampling: reduce & factor is not used")
        return da1.interp_like(da2, method="linear")


def rio_super_resolution(da, factor=2, dims=("x", "y"), method="linear", order=1):
    return da.interp({d: zoom(da[d], factor, order=order) for d in dims}, method=method)


def rio_scale_shape_transform(shape, transform, factor=10):
    (
        pixel_width,
        row_rot,
        x_upper_left,
        col_rot,
        pixel_height,
        y_upper_left,
    ) = transform[:6]
    transform = Affine(
        pixel_width / factor,
        row_rot,
        x_upper_left,
        col_rot,
        pixel_height / factor,
        y_upper_left,
    )
    shape = list(shape[-2:])
    shape[0] = shape[0] * factor
    shape[1] = shape[1] * factor
    return shape, transform


def rio_geom_to_xy_slice(geom, shape, transform):
    local_bounds = shapely.bounds(geom)
    if transform[4] < 0:  # if pixel_height is negative
        original_window = rasterio.windows.from_bounds(
            *local_bounds, transform=transform
        )
        gridded_window = rasterio.windows.round_window_to_full_blocks(
            original_window, [(1, 1)]
        )
        y_slice, x_slice = gridded_window.toslices()
        return x_slice, y_slice
    else:  # if pixel_height is not negative
        original_window = rasterio.windows.from_bounds(
            *local_bounds,
            transform=Affine(
                transform[0],
                transform[1],
                transform[2],
                transform[3],
                -transform[4],
                -transform[5],
            ),
        )
        gridded_window = rasterio.windows.round_window_to_full_blocks(
            original_window, [(1, 1)]
        )
        y_slice, x_slice = gridded_window.toslices()
        y_slice = slice(shape[0] - y_slice.stop, shape[0] - y_slice.start + 0)
        return x_slice, y_slice
