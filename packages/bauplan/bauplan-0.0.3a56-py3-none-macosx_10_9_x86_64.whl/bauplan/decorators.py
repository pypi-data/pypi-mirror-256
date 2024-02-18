import functools
from typing import Any, Callable, Dict, List, Optional


def model(
    name: Optional[str] = None,
    columns: Optional[List[str]] = None,
    materialize: Optional[bool] = None,
    internet_access: Optional[bool] = None,
) -> Callable:
    """Define a Bauplan Model.

    Args:
        name (Optional[str]): the name of the model (e.g. 'users'); if missing the function name is used
        columns (Optional[List[str]]): the columns of the model (e.g. ['id', 'name', 'email'])
        materialize (Optional[bool]): whether the model should be materialized
        internet_access (Optional[bool]): whether the model requires internet access
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def expectation() -> Callable:
    """Define a Bauplan Expectation.

    Args:
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def synthetic_model(
    name: str,
    columns: List[str],
) -> Callable:
    """Define a Bauplan Synthetic Model.

    Args:
        name (Optional[str]): the name of the model (e.g. 'users'); if missing the function name is used
        columns (List[str]): the columns of the synthetic model (e.g. ['id', 'name', 'email'])
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def python(
    version: Optional[str] = None,
    pip: Optional[Dict[str, str]] = None,
) -> Callable:
    """Define a Bauplan Expecation.

    Args:
        version (str): the python version required to run the model (e.g. '3.11')
        pip (Optional[List[Callable]]): a list of python depedencies to install into the model function (e.g. {'requests': '2.26.0'})
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator
