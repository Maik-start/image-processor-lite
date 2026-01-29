Native extension build instructions

Prerequisites (Debian/Ubuntu):

- build-essential
- python3-dev (matching the Python interpreter used to build)
- pip, setuptools

Install prerequisites example:

sudo apt update && sudo apt install -y build-essential python3-dev

Build (from project root `package_dev` using virtualenv python):

```bash
# from workspace/package_dev
./.venv/bin/python imgprocessor/visual_analysis/setup_native.py build_ext --inplace
```

Or use the helper script:

```bash
./build_native.sh /path/to/python
```

Notes:
- The supplied `native_stub.c` is a scaffold with placeholders. Replace with optimized C/C++ implementations for `segment_by_color` and `compute_chromatic_stability`.
- If build fails with `Python.h: No such file`, install the `python3-dev` package for your system Python.
- The package will automatically fall back to the pure-Python implementations if the native extension is not available.
