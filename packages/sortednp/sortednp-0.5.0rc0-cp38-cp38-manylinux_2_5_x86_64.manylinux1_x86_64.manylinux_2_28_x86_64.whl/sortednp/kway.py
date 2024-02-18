from typing import Callable, Sequence, Union

import numpy as np
import sortednp._internal as _internal

DeferredArray = Union[np.ndarray, Callable]


def resolve(obj: DeferredArray) -> np.ndarray:
    """
    Helper function to check whether the given object is callable. If yes,
    return its return value, otherwise return the object itself.

    This function is used by the package to load large datasets on demand to
    avoid out-of-memory scenarios.
    """
    return obj() if callable(obj) else obj


def merge(
    *arrays: Sequence[DeferredArray], assume_sorted: bool = True, **kwds
):
    """
    Return a sorted array containing the union of all input arrays.

    If the optional flag assume_sorted is set to False, the function sorts the
    arrays before merging.

    The method raises a TypeError, if the array count is zero.

    The arguments can load the arrays on the fly. If an argument is callable,
    its return value is used as an array instead of the argument itself. This
    makes it possible to load one array after another to avoid having all
    arrays in memory at the same time.

    !!! note
        Note on the performance: The function merges the arrays one-by-one.
        This is not the most performant implementation.

    Parameters
    ----------
    *arrays : np.ndarray or callable
        The arrays to merge as numpy arrays or deferred arrays.
    assume_sorted : bool, optional
        If True, the function assumes that the arrays are sorted. If False, the
        function sorts the arrays before merging. The default is True.
    **kwds : dict
        Any other keyword argument is passed to the native
        [merge][sortednp.merge] function.

    Returns
    -------
    np.ndarray
        The merged array.
    """
    if not arrays:
        raise TypeError("Merge expects at least one array.")

    arrays: list = list(arrays)
    merge_result = arrays.pop()
    merge_result = resolve(merge_result)
    if not assume_sorted:
        merge_result.sort()
    for array in arrays:
        array = resolve(array)
        if not assume_sorted:
            array.sort()
        merge_result = _internal.merge(merge_result, array, **kwds)
    return merge_result


def intersect(
    *arrays: Sequence[DeferredArray], assume_sorted: bool = True, **kwds
):
    """
    Return a sorted array containing the intersection of all input arrays.

    If the optional flag assume_sorted is set to False, the function sorts the
    arrays prior to intersecting. The arrays are order by increasing size
    before starting to intersection the arrays one-by-one.

    The method raises a TypeError, if the array count is zero.

    The arguments can load the arrays on the fly. If an argument is callable,
    its return value is used as an array instead of the argument itself. This
    makes it possible to load one array after another to avoid having all
    arrays in memory at the same time. Arrays deferred in this way, are loaded
    only after all in-memory arrays are intersected. The computed intersection
    is empty at any point, the function stops and returns an empty array.

    !!! note
        Note on the performance: The function intersects the arrays one-by-one.
        This is not the most performant implementation.

    Parameters
    ----------
    *arrays : np.ndarray or callable
        The arrays to intersect as numpy arrays or deferred arrays.
    assume_sorted : bool, optional
        If True, the function assumes that the arrays are sorted. If False, the
        function sorts the arrays before intersecting. The default is True.
    **kwds : dict
        Any other keyword argument is passed to the native
        [intersect][sortednp.intersect] function.

    Returns
    -------
    np.ndarray
        The union array.
    """

    if not arrays:
        raise TypeError("Merge expects at least one array.")

    # start with smallest non-callable
    inf = float("inf")
    len_array = [(inf if callable(a) else len(a), a) for a in arrays]
    len_array = sorted(len_array, key=lambda x: x[0])
    arrays = [a for _, a in len_array]

    intersect_result = arrays.pop()
    intersect_result = resolve(intersect_result)
    if not assume_sorted:
        intersect_result.sort()
    for array in arrays:
        if len(intersect_result) == 0:
            break
        array = resolve(array)
        if not assume_sorted:
            array.sort()
        intersect_result = _internal.intersect(intersect_result, array, **kwds)
    return intersect_result
