import sys

import numpy as np
import xarray
from scipy.spatial import KDTree


def rio_distance(
    dataset: xarray.Dataset,
    variable: str,
    suffix: str = "_distance",
    coords_x: str = "x",
    coords_y: str = "y",
    chunk_size: int = 500_000,
    verbose: bool = False,
) -> xarray.Dataset:
    df = dataset[variable].to_dataframe().reset_index()
    df2 = df[df[variable] == 1]
    if len(df2) == 0:
        return xarray.DataArray(
            dataset[variable].values + np.inf,
            name=variable + suffix,
            coords=dataset[variable].coords,
        )
    tree = KDTree(np.vstack(list(zip(df2[coords_x].values, df2[coords_y].values))))
    df["dist"] = 0
    n_chunk = (len(df) // chunk_size) + 1
    for i in range(n_chunk):
        if verbose:
            sys.stdout.write(f"\r{i+1} of {n_chunk}")
        tmp = df.iloc[i * chunk_size : (i + 1) * chunk_size]
        distances, indices = tree.query(
            np.vstack(list(zip(tmp[coords_x].values, tmp[coords_y].values))), k=1
        )
        df.iloc[
            i * chunk_size : (i + 1) * chunk_size, -1
        ] = distances  # [:,-1] guarantees [:,'dist']
    if verbose:
        print(" done!")
    return xarray.DataArray(
        df.dist.values.reshape(dataset[variable].shape),
        name=variable + suffix,
        coords=dataset[variable].coords,
    )
