[![Unit Tests](https://github.com/Pressio/pressio-linalg/actions/workflows/test.yaml/badge.svg)](https://github.com/Pressio/pressio-linalg/actions/workflows/test.yaml/badge.svg)

# pressio-linalg

## Overview

This Python library offers basic linear algebra functions that can be implemented in parallel.

## Installation

`pressio-linalg` is tested on Python 3.8-3.11.

To install, use the following command:

```
pip install pressio-linalg
```

With this installation, all kernels are implemented with pure Python calls and calls to MPI. This ensures that all the communication is handled explicitly internally and we do not rely on any external backend.
