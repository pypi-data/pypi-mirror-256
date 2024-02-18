"""
Sortednp (sorted numpy) is a python package which provides methods to perform
efficient set operations on sorted numpy arrays. This includes intersecting
and merging sorted numpy arrays. The returned intersections and unions are
also sorted.
"""

import enum
from typing import Any, Union, Tuple
import numpy as np
from sortednp import _internal
from .kway import resolve
from .kway import intersect as kway_intersect
from .kway import merge as kway_merge


__all__ = [
    "Algorithms",
    "IntersectDuplicates",
    "MergeDuplicates",
    "SubsetDuplicates",
    "isitem",
    "issubset",
    "intersect",
    "merge",
    "resolve",
    "kway_intersect",
    "kway_merge",
]


__version__ = "0.5.0-rc"  # Also change in setup.py


class Algorithms(enum.IntEnum):
    """
    Intersections are calculated by iterating both arrays. For a given element
    in one array, the method needs to search the other and check if the element
    is contained. In order to make this more efficient, we can use the fact
    that the arrays are sorted. There are three search methods, which can be
    selected via the optional keyword argument `algorithm`.
    """

    SIMPLE_SEARCH = 1
    """
    Search for an element by linearly iterating over the array
    element-by-element. [More
    Information](https://en.wikipedia.org/wiki/Linear_search).
    """

    BINARY_SEARCH = 2
    """
    Slice the remainder of the array in halves and repeat the procedure on
    the slice which contains the searched element. [More
    Information](https://en.wikipedia.org/wiki/Binary_search_algorithm).
    """

    GALLOPING_SEARCH = 3
    """
    First, search for an element linearly, doubling the step size after each
    step. If a step goes beyond the search element, perform a binary search
    between the last two positions. [More
    Information](https://en.wikipedia.org/wiki/Exponential_search).
    """


# Short-hand access for backwards compatibility
SIMPLE_SEARCH = Algorithms.SIMPLE_SEARCH
BINARY_SEARCH = Algorithms.BINARY_SEARCH
GALLOPING_SEARCH = Algorithms.GALLOPING_SEARCH


class IntersectDuplicates(enum.IntEnum):
    """
    Specify how to handle duplicated items in the input arrays when computing
    their intersection.
    """

    DROP = 4
    """
    With [DROP][sortednp.IntersectDuplicates.DROP], the intersection ignore
    any duplicated entries. The output will contain only unique values.
    """

    KEEP_MIN_N = 5
    """
    With [KEEP_MIN_N][sortednp.IntersectDuplicates.KEEP_MIN_N], if an item
    occurs `n > 0` times in one input array and `m > 0` times in the other
    array, the output will contain the item `min(n, m)` times.
    """

    KEEP_MAX_N = 7
    """
    With [KEEP_MAX_N][sortednp.IntersectDuplicates.KEEP_MAX_N], the
    intersection an item occurs `n > 0` times in one input array and `m > 0`
    times in the other array, the output will contain the item `min(n, m)`
    times.
    """


# Short-hand access for backwards compatibility
DROP = IntersectDuplicates.DROP
KEEP_MIN_N = IntersectDuplicates.KEEP_MIN_N
KEEP_MAX_N = IntersectDuplicates.KEEP_MAX_N


class MergeDuplicates(enum.IntEnum):
    """
    Specify how to handle duplicated items in the input arrays during merging.
    """

    DROP = 4
    """
    Ignore any duplicated elements. The output contains only unique values.
    """

    DROP_IN_INPUT = 6
    """
    Ignores duplicated elements in the input arrays separately. This is the
    same as ensuring that each input array unique values. The output contains
    every value at most twice.
    """

    KEEP = 8
    """
    Keep all duplicated entries. If an item occurs `n` times in one input
    array and `m` times in the other input array, the output contains the item
    `n + m` times.
    """


# Short-hand access for backwards compatibility
DROP_IN_INPUT = MergeDuplicates.DROP_IN_INPUT
KEEP = MergeDuplicates.KEEP


class SubsetDuplicates(enum.IntEnum):
    """
    Procedure to handle duplicates for issubset() function.
    """

    IGNORE = 9
    """
    Ignore duplicates in the potential subset and the superset arrays. The
    [issubset()][sortednp.issubset] function returns true if every unique
    values in the first array exists **at least once** in the superset array.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([2, 2])
    b = np.array([2])

    assert snp.issubset(a, b, duplicates=snp.SubsetDuplicates.IGNORE)
    assert snp.issubset(b, a, duplicates=snp.SubsetDuplicates.IGNORE)
    ```
    """

    REPEAT = 10
    """
    Account for the number of occurrences of each item in the potential subset.
    The [issubset()][sortednp.issubset] function returns true if and only if
    every item in the first array appears **at least as often** in the superset
    array as it is contained in the subset array.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([2])
    b = np.array([2, 2])

    assert snp.issubset(a, b, duplicates=snp.SubsetDuplicates.REPEAT)
    assert not snp.issubset(b, a, duplicates=snp.SubsetDuplicates.REPEAT)
    ```
    """


# Short-hand access for backwards compatibility
IGNORE = SubsetDuplicates.IGNORE
REPEAT = SubsetDuplicates.REPEAT


def isitem(
    element: Any, array: np.ndarray, algorithm=Algorithms.GALLOPING_SEARCH
):
    """
    Returns True if element is contained in the array, otherwise False.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([1, 2, 3])
    assert snp.isitem(1, a)
    assert not snp.isitem(4, a)
    ```

    The algorithm parameter determines the search algorithm to use. See
    [Algorithms][sortednp.Algorithms] for possible values. The default is
    [GALLOPING_SEARCH][sortednp.Algorithms.GALLOPING_SEARCH].

    !!! warning
        Please note that the search element is casted to the numpy type of the
        given array. This might lead to unexpected results if the element is
        outside the domain of the date type.

        ```python
        a = np.array([1, 2, 255], dtype=np.unit8)
        assert snp.isitem(-1, a)  # -1 turns into 255
        ```

        [Future numpy versions](https://numpy.org/devdocs/release/1.24.0-notes.
        html#conversion-of-out-of-bound-python-integers)
        will raise an Exception.

    Parameters
    ----------
    element : Any
        The element to search in array
    array : np.ndarray
        The sorted array to search the element. Adjacent items must be in
        ascending order. The behavior of the function is undefined if the array
        is not sorted.
    algorithm : int
        The algorithm to use for the search. See
        [Algorithms][sortednp.Algorithms] for possible values.

    Returns
    -------
    bool
        True if subset is a subset of array, otherwise False.
    """
    return issubset(
        np.array([element], dtype=array.dtype), array, algorithm=algorithm
    )


def issubset(
    subset: np.ndarray,
    array: np.ndarray,
    algorithm: Algorithms = Algorithms.GALLOPING_SEARCH,
    duplicates: SubsetDuplicates = SubsetDuplicates.IGNORE,
):
    """
    Returns True if all values in `subset` appear in `array`,
    i.e., return True if `subset` is a subset of `array`, otherwise False.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([1, 3])
    b = np.array([1, 2, 3])
    assert snp.issubset(a, b)
    ```

    The `algorithm` parameter determines the search algorithm to use. See
    [Algorithms][sortednp.Algorithms] for possible values. The default is
    [GALLOPING_SEARCH][sortednp.Algorithms.GALLOPING_SEARCH].

    If `duplicates` is
    [SubsetDuplicates.IGNORE][sortednp.SubsetDuplicates.IGNORE], returns True
    if and only if each unique element in `subset` appears at least once in
    `array`.

    ```python
    a = np.array([2])
    b = np.array([2, 2])
    assert snp.issubset(a, b, duplicates=snp.SubsetDuplicates.IGNORE)
    assert snp.issubset(b, a, duplicates=snp.SubsetDuplicates.IGNORE)
    ```

    If `duplicates` is
    [SubsetDuplicates.REPEAT][sortednp.SubsetDuplicates.REPEAT], returns True
    if and only if each unique element in `subset` appears at least as often
    in `array` as it appears in `subset`.

    ```python
    a = np.array([2])
    b = np.array([2, 2])
    assert snp.issubset(a, b, duplicates=snp.SubsetDuplicates.REPEAT)
    assert not snp.issubset(b, a, duplicates=snp.SubsetDuplicates.REPEAT)
    ```

    Parameters
    ----------
    subset : np.ndarray
        The potential subset in question.
    array : np.ndarray
        The sorted array to check if subset is a true subset. Adjacent items
        must be in ascending order. The behavior of the function is undefined
        if the array is not sorted.
    algorithm : int
        The algorithm to use for the search. See Algorithms for possible
        values.
    duplicates : int
        How to handle duplicates. See Duplicates for possible values.

    Returns
    -------
    bool
        True if subset is a subset of array, otherwise False.
    """
    return _internal.issubset(
        subset, array, algorithm=algorithm, duplicates=duplicates
    )


def intersect(
    a: np.ndarray,
    b: np.ndarray,
    algorithm=Algorithms.GALLOPING_SEARCH,
    duplicates=IntersectDuplicates.KEEP_MIN_N,
    indices: bool = False,
) -> Union[np.ndarray, Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]]:
    """
    Return a sorted array with all elements that appear in both a and b, i.e.,
    it computes the intersection of a and b.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([1, 3, 5])
    b = np.array([1, 2, 3])
    assert snp.intersect(a, b).tolist() == [1, 3]
    ```

    The `algorithm` parameter determines the search algorithm to use. See
    [Algorithms][sortednp.Algorithms] for possible values. The default is
    [GALLOPING_SEARCH][sortednp.Algorithms.GALLOPING_SEARCH].

    If `duplicates` is set to [DROP][sortednp.IntersectDuplicates.DROP], the
    return value contains only unique values that appear in both input arrays.
    This behavior represents mathematical set intersection and ignores any
    duplication in the input.

    ```python
    a = np.array([2, 2])
    b = np.array([2, 2, 2])

    intersection = snp.intersect(
        a, b,
        duplicates=snp.IntersectDuplicates.DROP
    )
    assert intersection.tolist() == [2]
    ```

    If `duplicates` is set to
    [KEEP_MIN_N][sortednp.IntersectDuplicates.KEEP_MIN_N], the return value
    contains each item `min(n, m)` times, where `n` and `m` are the number of
    occurrences in array `a` and `b` respectively. The rational is that
    each duplicated item in the input arrays matches exactly once with an item
    in the other array. For example, consider:

    ```python
    a = np.array([2, 2])
    b = np.array([2, 2, 2])

    intersection = snp.intersect(
        a, b,
        # That's the default behavior
        duplicates=snp.IntersectDuplicates.KEEP_MIN_N
    )
    assert intersection.tolist() == [2, 2]
    ```

    The first `2` in array `a` matches with the first `2` in array `b`. The
    second `2` in array `a` matches with the second `2` in array `b`. However,
    the third `2` in array `b` has no match in array `a`. The previous
    duplications are already *taken*.

    If `duplicates` is set to
    [KEEP_MAX_N][sortednp.IntersectDuplicates.KEEP_MAX_N], the return value
    contains each item `max(n, m)` times, where `n` and `m` are the number of
    occurrences in array `a` and `b` respectively. The rational is that
    duplicates items in one input array can all match with a single item in the
    other array. For example, consider:

    ```python
    a = np.array([2, 2])
    b = np.array([2, 2, 2])

    intersection = snp.intersect(
        a, b,
        duplicates=snp.IntersectDuplicates.KEEP_MAX_N
    )
    assert intersection.tolist() == [2, 2, 2]
    ```

    For every occurrence of `2` in array `b`, we can verify that the element,
    i.e., `2`, is contained in array `a`.

    If the optional parameter `indices` is set to `True`, the function returns
    the intersection array and a tuple of arrays with integer indices. For
    each element in the intersection, the corresponding indices point to the
    position where the element is contained in the input arrays. Assuming
    `intersection, (indices_a, indices_b) = snp.intersect(a, b, indices=True)`,
    the following conditions hold for all `i` in the valid range.

    ```python
    intersection[i] == a[indices_a[i]]
    intersection[i] == b[indices_b[i]]
    ```

    Parameters
    ----------
    a : np.ndarray
        First array to intersect
    b : np.ndarray
        Second array to intersect
    algorithm : Algorithms
        Search algorithm to search common items in the arrays
    duplicates : IntersectDuplicates
        Specifies how to handle duplicated items in the input arrays
    indices : bool
        If True, return the indices of the intersection items in the input
        arrays.

    Returns
    -------
    Union[np.ndarray, tuple[np.ndarray, tuple[np.ndarray, np.ndarray]]]
        The intersection of the input arrays. If `indices` is set to `True`,
        the function returns a tuple containing the intersection array and a
        tuple of arrays with integer indices.
    """

    return _internal.intersect(
        a, b, algorithm=algorithm, duplicates=duplicates, indices=indices
    )


def merge(
    a: np.ndarray,
    b: np.ndarray,
    duplicates=MergeDuplicates.KEEP,
    indices: bool = False,
):
    """
    Return a sorted array containing all elements from both arrays.

    ```python
    import numpy as np
    import sortednp as snp

    a = np.array([2, 4])
    b = np.array([1, 2, 3])
    assert snp.merge(a, b).tolist() == [1, 2, 2, 3, 4]
    ```

    The `algorithm` parameter determines the search algorithm to use. See
    [Algorithms][sortednp.Algorithms] for possible values. The default is
    [GALLOPING_SEARCH][sortednp.Algorithms.GALLOPING_SEARCH].

    If `duplicates` is set to [DROP][sortednp.MergeDuplicates.DROP], the
    any duplicates in the merged output are omitted. The return values
    only contains unique values.

    ```python
    a = np.array([2, 2, 2])
    b = np.array([2, 2, 2, 2])

    merged = snp.merge(
        a, b,
        sortednp.MergeDuplicates.DROP
    )

    assert merged.tolist() == [2]
    ```

    If `duplicates` is set to
    [DROP_IN_INPUT][sortednp.MergeDuplicates.DROP_IN_INPUT], the output is
    obtained by merging the unique values from the input arrays. Values occur
    at most twice in the output. A value appearing twice in the output implies
    it exists in both input arrays.

    ```python
    a = np.array([2, 2, 2, 3, 3])
    b = np.array([2, 2, 2, 2])

    merged = snp.merge(
        a, b,
        sortednp.MergeDuplicates.KEEP_IN_INPUT
    )

    assert merged.tolist() == [2, 2, 3]
    ```

    If `duplicates` is set to [DROP][sortednp.MergeDuplicates.KEEP], the
    retains any duplication in the input arrays. If an item occurs `n` times
    in one input array and `m` times in the other input array, the output
    contains the item `n + m` times.

    ```python
    a = np.array([2, 2, 3, 3])
    b = np.array([2, 2, 2])

    merged = snp.merge(
        a, b,
        sortednp.MergeDuplicates.KEEP_IN_INPUT
    )

    assert merged.tolist() == [2, 2, 2, 2, 2, 3, 3]
    ```

    If the optional parameter `indices` is set to `True`, the function returns
    the union array and a tuple of arrays with integer indices. For
    each element in the union, the corresponding indices point to the
    position where the element is contained in the input arrays. Assuming
    `union, (indices_a, indices_b) = snp.merge(a, b, indices=True)`,
    the following conditions hold for all `i` in the valid range.

    ```python
    union[i] == a[indices_a[i]]
    union[i] == b[indices_b[i]]
    ```

    Parameters
    ----------
    a : np.ndarray
        First array to merge
    b : np.ndarray
        Second array to merge
    duplicates : MergeDuplicates
        Specifies how to handle duplicated items in the input arrays
    indices : bool
        If True, return the indices of the union items in the input
        arrays.

    Returns
    -------
    Union[np.ndarray, tuple[np.ndarray, tuple[np.ndarray, np.ndarray]]]
        The union of the input arrays. If `indices` is set to `True`,
        the function returns a tuple containing the union array and a
        tuple of arrays with integer indices.
    """
    return _internal.merge(a, b, duplicates=duplicates, indices=indices)
