import base64
import functools
import hashlib
import inspect
import os
import pickle
import types
from pathlib import Path
from typing import Callable

from loguru import logger

BASE_PATH = "/mnt/cache"


def _serialize_code(code: types.CodeType) -> bytes:
    func_code_bytes = base64.b64encode(code.co_code)

    # Introduce variable values into hash.
    func_const_values = [
        # Embedded lambdas must be serialized, same as the overall function
        (
            _serialize_code(const)
            if isinstance(const, types.CodeType)
            else str(const).encode("utf-8")
        )
        for const in code.co_consts
    ]
    # Names must be serialized as otherwise referenced names (min vs max) would not
    # affect cache key.
    func_name_values = [name.encode("utf-8") for name in code.co_names]

    return b"".join(
        [
            func_code_bytes,
            *func_const_values,
            *func_name_values,
        ]
    )


def _serialize_function_defaults(func: Callable) -> bytes:
    parts = []

    if func.__defaults__ is not None:
        for d in func.__defaults__:
            parts.append(_hashify(d).encode("utf-8"))

    if func.__kwdefaults__ is not None:
        for key, value in func.__kwdefaults__.items():
            parts.append(f"{key}{_hashify(value)}".encode("utf-8"))

    return b"".join(parts)


def _hashify(func) -> str:
    hash_object = hashlib.sha256()
    try:
        if hasattr(func, "__fused_cached_fn"):
            return _hashify(func.__fused_cached_fn)
        elif callable(func):
            hash_object.update(_serialize_code(func.__code__))
            # Caution! The defaults and args do not go into the same part of the cache key!
            hash_object.update(_serialize_function_defaults(func))
        else:
            hash_object.update(str(func).encode("utf-8"))
        return hash_object.hexdigest()
    except Exception as e:
        logger.warning(f"Error Hashing {e}")
        return ""


def _cache(
    func: Callable,
    *args,
    reset: bool = False,
    path: str = "tmp",
    retry: bool = True,
    **kwargs,
):
    path = path.strip("/")
    # Cache in mounted drive if available & writable, else cache in /tmp
    if Path(BASE_PATH).exists() and os.access(BASE_PATH, os.W_OK):
        base_path = Path(BASE_PATH)
    else:
        base_path = Path("/tmp")

    # Cache directory
    # TODO: consider udf name in path once available from Fused global context
    path = Path(base_path) / "cached_data" / path
    path.mkdir(parents=True, exist_ok=True)

    # Pop reserved `_cache_id`kwarg
    _cache_id = kwargs.pop("_cache_id", None)

    try:
        # TODO: ignore `_`

        # 1. Hashify function
        id = _hashify(func)

        # 2. Hashify args
        for v in args:
            id += "_" + _hashify(v)

        # 3. Hashify kwargs
        for k in kwargs:
            id += k + _hashify(kwargs[k])

        # 4. Hashify _cache_id
        id += _hashify(_cache_id)

        # 5. Hashify composite id
        id = _hashify(id)

        path_file = path / f"data_{id}"

        if not os.path.exists(path) or reset:
            with open(path_file, "wb") as f:
                data = func(*args, **kwargs)
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                return data
        else:
            try:
                with open(path_file, "rb") as f:
                    data = pickle.load(f)

                    return data
            except Exception as e:
                logger.debug(f"Error {e}. Retrying.")
                if retry:
                    with open(path_file, "wb") as f:
                        data = func(*args, **kwargs)
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                        return data
                else:
                    return None
    except Exception as e:
        logger.info(f"Error Caching {e}")
        raise e


async def _cache_async(
    func: Callable,
    *args,
    reset: bool = False,
    path: str = "tmp",
    retry: bool = True,
    **kwargs,
):
    path = path.strip("/")
    # Cache in mounted drive if available & writable, else cache in /tmp
    if Path(BASE_PATH).exists() and os.access(BASE_PATH, os.W_OK):
        base_path = Path(BASE_PATH)
    else:
        base_path = Path("/tmp")

    # Cache directory
    # TODO: consider udf name in path once available from Fused global context
    path = Path(base_path) / "cached_data" / path
    path.mkdir(parents=True, exist_ok=True)

    # Pop reserved `_cache_id`kwarg
    _cache_id = kwargs.pop("_cache_id", None)

    try:
        # TODO: ignore `_`

        # 1. Hashify function
        id = _hashify(func)

        # 2. Hashify args
        for v in args:
            id += "_" + _hashify(v)

        # 3. Hashify kwargs
        for k in kwargs:
            id += k + _hashify(kwargs[k])

        # 4. Hashify _cache_id
        id += _hashify(_cache_id)

        # 5. Hashify composite id
        id = _hashify(id)

        path_file = path / f"data_{id}"

        if not os.path.exists(path) or reset:
            with open(path_file, "wb") as f:
                data = await func(*args, **kwargs)
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                return data
        else:
            try:
                with open(path_file, "rb") as f:
                    data = pickle.load(f)

                    return data
            except Exception as e:
                logger.debug(f"Error {e}. Retrying.")
                if retry:
                    with open(path_file, "wb") as f:
                        data = await func(*args, **kwargs)
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                        return data
                else:
                    return None
    except Exception as e:
        logger.info(f"Error Caching {e}")
        raise e


def _cache_internal(func, **decorator_kwargs):
    def decorator(func):
        _path = decorator_kwargs.get("path", "tmp")

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def wrapper_async(*args, **kwargs):
                return await _cache_async(func, *args, path=_path, **kwargs)

            wrapper_async.__fused_cached_fn = func

            return wrapper_async
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return _cache(func, *args, path=_path, **kwargs)

            wrapper.__fused_cached_fn = func

            return wrapper

    if callable(func):  # w/o args
        return decorator(func)
    else:  # w/ args
        return decorator


def cache(func=None, **kwargs):
    return _cache_internal(func=func, **kwargs)


def cache_call(func, *args, **kwargs):
    return _cache(func, *args, **kwargs)


async def cache_call_async(func, *args, **kwargs):
    return await _cache_async(func, *args, **kwargs)
