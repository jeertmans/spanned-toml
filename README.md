[![Build Status](https://github.com/jeertmans/spanned-toml/workflows/Tests/badge.svg?branch=master)](https://github.com/jeertmans/spanned-toml/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/jeertmans/spanned-toml/branch/master/graph/badge.svg)](https://codecov.io/gh/jeertmans/spanned-toml)
[![PyPI version](https://img.shields.io/pypi/v/spanned-toml)](https://pypi.org/project/spanned-toml)

# Spanned-Toml

> A lil' TOML parser, but with span

This project is an extension of
[@hukkin's Tomli](https://github.com/hukkin/tomli) libray, but with span.

A span is simply a Python `slice` that helps to retrieve where a given object
was parsed from.

## Motivation<a name="motivation"></a>

TOML has become a popular format for configuration files, and many tools now
rely on parsing such files. However, most parsers error on invalid TOML syntax,
not configuration specific errors. E.g., what happens with the following file?

```toml
age = -45  # age should be a positive integer
```

First, you parse the TOML file, which is valid, then you invalidate the `age`
value because it is negative. But how to pinpoint the location of where `age`
was defined to the user?

This is where Spanned-Toml comes into play. For every key / value, you can
obtain the span information about where it was defined. The span is simple a
Python `slice`, that can be used to index the original TOML string.

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Motivation](#motivation)
- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
- [Why choosing Spanned-Toml over others?](#why-choosing-spanned-toml-over-others)
- [Versions](#versions)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

Spanned-Toml is a Python library for parsing [TOML](https://toml.io), with the
**only** addition of span information for every object (both keys and values).
It is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0), and its
goal is to provide span information with minimal overhead over Tomli.

As such, Spanned-Toml provides the same features and API as Tomli, with the only
difference is that it returns a `Spanned[dict]`, instead of `dict`.

If you whish to get the same output as with Tomli, you can always call `.unspan()`
on a `Spanned` object.

## Installation<a name="installation"></a>

```bash
pip install spanned-toml
```

## Usage<a name="usage"></a>

Toml-Spanned has the **exact** same interface as Tomli. Therefore, I recommend
you checking [Tomli's usage](https://github.com/hukkin/tomli#usage).

The only addition is that, instead of returning an object `T`, it returns
`Spanned[T]`, and nested objects are also `Spanned`, i.e., array and dictionnary
values are also spanned.

From `Spanned[T]`, you can always obtain the inner value `T` with `.inner()`:

```python
import spanned_toml as toml

toml_dict = toml.loads("age = 10")

assert toml_dict["age"].inner() == 10
```

> NOTE: for convenience, `Spanned[T]` inherits most attributes from `T`.

If you have nested `Spanned` objects, then you can call `.unspan()` to remove
all span information, and obtain the same object as if you used Tomli.

```python
toml_str = """
[[players]]
name = "Lehtinen"
number = 26

[[players]]
name = "Numminen"
number = 27
"""

toml_dict = toml.loads(toml_str).unspan()
assert toml_dict == {
    "players": [{"name": "Lehtinen", "number": 26}, {"name": "Numminen", "number": 27}]
}
```

Last, but not least, you can retrieve the exact part of the string that was used
to parse a given key or value.

```python
player_span = toml_dict["players"][0]["name"].span()

assert toml_str[player_span] == '"Lehtinen"'  # Quotes are included in span
```

> NOTE: arrays of tables have an empty span, since then can be defined in
> multiple parts of a given file.

## Why choosing Spanned-Toml over others?<a name="why-choosing-spanned-toml-over-others"></a>

Spanned-Toml was mainly built for another project I am working on.

You should use this package whenever you care about where specific parts in a
TOML config file are coming from. This might be useful, e.g., if you want to
have a validation layer, on top of the default TOML, and that you want to exactly
pinpoint where an error originated.

Otherwise, if you just care about parsing TOML file or speed, then directly use
Tomli (or other faster alternatives).

## Versions<a name="versions"></a>

Toml-Spanned follows the same versions as Tomli, and tries to be in sync with it.

Therefore, Tomli-Spanned's version `X.Y.Z.P` matches Tomli's version `X.Y.Z`.
The `P` number of for patches, and is only intended to fix issues related to span.
