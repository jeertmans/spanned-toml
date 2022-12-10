[![Build Status](https://github.com/jeertmans/spanned-toml/workflows/Tests/badge.svg?branch=master)](https://github.com/jeertmans/spanned-toml/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/jeertmans/spanned-toml/branch/master/graph/badge.svg)](https://codecov.io/gh/jeertmans/spanned-toml)
[![PyPI version](https://img.shields.io/pypi/v/spanned-toml)](https://pypi.org/project/spanned-toml)

# Spanned-Toml

> A lil' TOML parser, but with span

This project is an extension of @hukkin's Tomli libray, but with span.

A span is simply a Python `slice` that helps to retrieve where a given object
was parsed from.

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
  - [Parse a TOML string](#parse-a-toml-string)
  - [Parse a TOML file](#parse-a-toml-file)
  - [Handle invalid TOML](#handle-invalid-toml)
  - [Construct `decimal.Decimal`s from TOML floats](#construct-decimaldecimals-from-toml-floats)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

Spanned-Toml is a Python library for parsing [TOML](https://toml.io), with the
addition of span information for every object (both keys and values).
It is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).

spanned-Toml provides the same features and API as Tomli. The only difference
is that it returns a `Spanned[dict]`, instead of `dict`.

If you whish to get the same output as with Tomli, you can always call `unspan()`
on a `Spanned` object.

## Installation<a name="installation"></a>

```bash
pip install tomli
```

## Usage<a name="usage"></a>

### Parse a TOML string<a name="parse-a-toml-string"></a>

```python
import tomli

toml_str = """
[[players]]
name = "Lehtinen"
number = 26

[[players]]
name = "Numminen"
number = 27
"""

toml_dict = tomli.loads(toml_str).unspan()
assert toml_dict == {
    "players": [{"name": "Lehtinen", "number": 26}, {"name": "Numminen", "number": 27}]
}
```

### Parse a TOML file<a name="parse-a-toml-file"></a>

```python
import tomli

with open("path_to_file/conf.toml", "rb") as f:
    toml_dict = tomli.load(f)
```

The file must be opened in binary mode (with the `"rb"` flag).
Binary mode will enforce decoding the file as UTF-8 with universal newlines disabled,
both of which are required to correctly parse TOML.

### Handle invalid TOML<a name="handle-invalid-toml"></a>

```python
import tomli

try:
    toml_dict = tomli.loads("]] this is invalid TOML [[")
except tomli.TOMLDecodeError:
    print("Yep, definitely not valid.")
```

Note that error messages are considered informational only.
They should not be assumed to stay constant across Tomli versions.

### Construct `decimal.Decimal`s from TOML floats<a name="construct-decimaldecimals-from-toml-floats"></a>

```python
from decimal import Decimal
import tomli

toml_dict = tomli.loads("precision-matters = 0.982492", parse_float=Decimal).unspan()
assert isinstance(toml_dict["precision-matters"], Decimal)
assert toml_dict["precision-matters"] == Decimal("0.982492")
```

Note that `decimal.Decimal` can be replaced with another callable that converts a TOML float from string to a Python type.
The `decimal.Decimal` is, however, a practical choice for use cases where float inaccuracies can not be tolerated.

Illegal types are `dict` and `list`, and their subtypes.
A `ValueError` will be raised if `parse_float` produces illegal types.
