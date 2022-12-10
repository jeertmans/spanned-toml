# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Jérome Eertmans, Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

__all__ = ("tomllib",)

# By changing this one line, we can run the tests against
# a different module name.
import spanned_toml as tomllib
tomllib.sp_loads = tomllib.loads
tomllib.loads = lambda *args, **kw: tomllib.sp_loads(*args, **kw).unspan()
