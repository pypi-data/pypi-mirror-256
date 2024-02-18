from __future__ import annotations

import warnings
from collections.abc import Iterable
from functools import cached_property
from typing import Any, Optional

from ._impl._context_impl import context_get_user_email
from ._impl._reimports import BaseUdf, UdfJobStepConfig
from ._impl._udf_ops_impl import get_step_config_from_server, run_and_get_data


class AttrDict(dict):
    """Dictionary where keys can also be accessed as attributes"""

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if __name in self:
                return self[__name]
            else:
                raise

    def __dir__(self) -> Iterable[str]:
        return self.keys()


class ExecutableUdf:
    def __init__(self, step_config: UdfJobStepConfig) -> None:
        self._step_config = step_config

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return run_and_get_data(self._udf, *args, **kwargs)

    def udf(self, *args: Any, **kwargs: Any) -> Any:
        return self(*args, **kwargs)

    @property
    def _udf(self) -> BaseUdf:
        return self._step_config.udf

    @cached_property
    def utils(self):
        if len(self._udf.headers) == 0:
            raise ValueError("UDF does not have a utils module")
        if len(self._udf.headers) > 1:
            raise ValueError("UDF has multiple header modules")
        if self._udf.headers[0].module_name != "utils":
            warnings.warn(
                f"Accessing header module {self._udf.headers[0].module_name} under the name utils"
            )
        # TODO: Even though this might have already been evaluated, we have to evaluate it again now
        # It is at least cached

        vals = self._udf.headers[0]._exec()

        return AttrDict(vals)

    def __str__(self) -> str:
        return f"<UDF {self._udf.name}>"


def import_udf(
    email_or_id: str, id: Optional[str] = None, *, cache_key: Any = None
) -> ExecutableUdf:
    """
    Download the code of a UDF, to be run inline.

    Args:
        email_or_id: Email of the UDF's owner, or name of the UDF to import.
        id: Name of the UDF to import. If only the first argument is provided, the current user's email will be used.

    Keyword args:
        cache_key: Additional cache key for busting the UDF cache
    """
    if id is None:
        id = email_or_id
        try:
            email = context_get_user_email()
        except Exception as e:
            raise ValueError(
                "could not detect user ID from context, please specify the UDF as 'user@example.com', 'udf_name'."
            ) from e
    else:
        email = email_or_id
    step_config = get_step_config_from_server(
        email=email,
        slug=id,
        cache_key=cache_key,
    )

    return ExecutableUdf(step_config=step_config)
