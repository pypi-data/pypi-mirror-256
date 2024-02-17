# Flower Crane

Flower Crane explores Python bindings in Rust. It has three implementations of the same function:

1. Native Python + NumPy
2. Rust Bindings into Python
3. Rust Bindings into NumPy

## Develop

First, create a new virtual env and activate it

```bash
python -m venv .env
source .env/bin/activate
```

You can install the module locally with

```bash
maturin develop
```

After you have placed your PyPi API-Token in your `.pypirc` file, you can publish your module with

```bash
maturin publish -r test
```

or 

```bash
maturin publish -r pypi
```

## Tests

```bash
python -m pytest
cargo test
```

## Benches

To compare the performances of the different implementations, run

```bash
maturin build --release
pip install .
python -m py_flower_crane.bench
```
