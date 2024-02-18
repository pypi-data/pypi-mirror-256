# Pseudo Bridgeland Tilt Python Package

This is a Python wrapper around a [Rust crate](https://gitlab.com/pseudowalls/tilt.rs) for computing a list of pseudo semistabilizers of a given Chern character (currently just on P^2).
Less feature-ful and tested as https://github.com/benjaminschmidt/stability_conditions, but much faster.

# Mathematics:

TODO

# Installation

This python package in published to [PyPI](https://pypi.org/manage/project/pseudo-bridgeland-tilt/releases/).
Install it via `pip` in a python3 or sage environment, e.g.:

```bash
sage -pip install pseudo_bridgeland_tilt
```
```bash
pip3 install pseudo_bridgeland_tilt
```

# Usage

```python
>>> from pseudo_tilt import pseudo_semistabilizers
>>> pseudo_semistabilizers(3, 2, -4)
```
which gives expected output:
```output
Computing pseudo semistabilizers for Chern Character: (3, 2ℓ, -4½ℓ²)

[(1, 0, 0), (4, -2, 1), (2, ...
```
