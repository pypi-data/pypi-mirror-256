from typing import Any, Optional

from fused.api.api import FusedAPI
from fused.models.api import UdfJobStepConfig
from fused.models.udf import BaseUdf


def get_step_config_from_server(
    email: str, slug: Optional[str], cache_key: Any
) -> UdfJobStepConfig:
    # cache_key is unused
    api = FusedAPI()
    obj = api._get_udf(email, slug)
    udf = BaseUdf.parse_raw(obj["udf_body"], content_type="json")

    step_config = UdfJobStepConfig(udf=udf)
    return step_config


def run_and_get_data(udf, *args, **kwargs):
    # TODO: This is a silly way to do this, because we have to pass parameters in such an odd way
    job = udf(*args, **kwargs)
    result = job.run_local()
    return result.data
