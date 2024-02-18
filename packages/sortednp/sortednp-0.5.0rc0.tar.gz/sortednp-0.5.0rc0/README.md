# Sortednp

The package to intersect or merge sorted numpy arrays.

[![Pipeline](https://gitlab.sauerburger.com/frank/sortednp/badges/main/pipeline.svg)](https://gitlab.sauerburger.com/frank/sortednp/-/pipelines)
[![Pylint](https://gitlab.sauerburger.com/frank/sortednp/-/jobs/artifacts/main/raw/pylint.svg?job=pylint)](https://gitlab.sauerburger.com/frank/sortednp)
[![C++ lint](https://gitlab.sauerburger.com/frank/sortednp/-/jobs/artifacts/main/raw/cxxlint.svg?job=cpplint)](https://gitlab.sauerburger.com/frank/sortednp)
[![License](https://gitlab.sauerburger.com/frank/sortednp/-/jobs/artifacts/main/raw/license.svg?job=badges)](https://gitlab.sauerburger.com/frank/sortednp/-/blob/main/LICENSE)
[![PyPI](https://gitlab.sauerburger.com/frank/sortednp/-/jobs/artifacts/main/raw/pypi.svg?job=badges)](https://pypi.org/project/sortednp/)

Numpy and Numpy arrays are a really great tool. However, intersecting and
merging multiple sorted numpy arrays is rather less performant. The current numpy
implementation concatenates the two arrays and sorts the combination. If you
want to merge or intersect multiple numpy arrays, there is a much faster way,
by using the property, that the resulting array is sorted.

Sortednp (sorted numpy) operates on sorted numpy arrays to calculate the
intersection or the union of two numpy arrays in an efficient way. The
resulting array is again a sorted numpy array, which can be merged or
intersected with the next array. The intended use case is that sorted numpy
arrays are sorted as the basic data structure and merged or intersected at
request. Typical applications include information retrieval and search engines
in particular.

It is also possible to implement a k-way merging or intersecting algorithm,
which operates on an arbitrary number of arrays at the same time. This package
is intended to deal with arrays with $`10^6`$ or $`10^{10}`$ items. Usually, these
arrays are too large to keep more than two of them in memory at the same
time. This package implements methods to merge and intersect multiple arrays,
which can be loaded on-demand.

## Links
- [Git Repository](https://gitlab.sauerburger.com/frank/sortednp)
- [Documentation](https://sortednp.dev)
- [PyPI](https://pypi.org/project/sortednp/)

## Installation from PyPI

You can install the package directly from PyPI using `pip`.

```bash
$ pip install sortednp
```

### Numpy Dependency
The installation fails in some cases, because of a build-time dependency on
numpy. Usually, the problem can be solved by manually installing a recent numpy
version via `pip install -U numpy`.

ju
## Basic Usage
### Two-way intersection

Two sorted numpy arrays can be intersected with the `intersect` method, which takes two
numpy arrays and returns the sorted intersection of the two arrays.

<!-- write intersect.py -->
```python
## intersect.py
import numpy as np
import sortednp as snp

a = np.array([0, 3, 4, 6, 7])
b = np.array([1, 2, 3, 5, 7, 9])

i = snp.intersect(a, b)
print(i)
```

If you run this, you should see the intersection of both arrays as a sorted numpy
array.
<!-- console_output -->
```python
$ python3 intersect.py
[3 7]
```

### Two-way union

Two numpy sorted arrays can be merged with the `merge` method, which takes two
numpy arrays and returns the sorted union of the two arrays.

<!-- write merge.py -->
```python
## merge.py
import numpy as np
import sortednp as snp

a = np.array([0, 3, 4, 6, 7])
b = np.array([1, 2, 3, 5, 7, 9])

m = snp.merge(a, b)
print(m)
```

If you run this, you should see the union of both arrays as a sorted numpy
array.
<!-- console_output -->
```python
$ python3 merge.py
[0 1 2 3 3 4 5 6 7 7 9]
```