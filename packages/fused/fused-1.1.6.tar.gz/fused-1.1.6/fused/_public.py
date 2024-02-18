from typing import Any, Union

from fused.utils import import_udf
from fused.utils._udf_ops import AttrDict


class _Public:
    def __init__(self, email: str, cache_key: Any = None):
        self._email = email
        self._cache_key = cache_key

    def __getattribute__(self, key: str) -> Union[Any, AttrDict]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __getitem__(self, key: str) -> AttrDict:
        return import_udf(self._email, id=key, cache_key=self._cache_key).utils


public = _Public("sina@fused.io")
