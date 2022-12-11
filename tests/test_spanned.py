# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Jérome Eertmans, Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

import unittest

from . import tomllib


class TestSpanned(unittest.TestCase):
    def test_basic(self):
        doc = "one=1 \n two='two' \n arr=[]"
        keys_expected = ["one", "two", "arr"]
        values_expected = ["1", "'two'", "[]"]

        for i, (key, value), in enumerate(tomllib.loads(doc).items()):
            got_key = doc[key.span()]
            got_value = doc[value.span()]
            self.assertEqual(got_key, keys_expected[i])
            self.assertEqual(got_value, values_expected[i])

    def test_advanced(self):
        doc = """
        data = [ ["delta", "phi"], [3.14] ]
        temp_targets = { cpu = 79.5, case = 72.0 }
        """
        toml = tomllib.loads(doc)

        self.assertEqual(doc[toml["data"].span()], '[ ["delta", "phi"], [3.14] ]')
        self.assertEqual(doc[toml["data"][0].span()], '["delta", "phi"]')
        self.assertEqual(doc[toml["data"][0][0].span()], '"delta"')
        self.assertEqual(doc[toml["data"][0][1].span()], '"phi"')
        self.assertEqual(doc[toml["data"][1].span()], "[3.14]")
        self.assertEqual(doc[toml["data"][1][0].span()], "3.14")

        d = toml["temp_targets"]
        k = list(d.keys())

        self.assertEqual(doc[d.span()], "{ cpu = 79.5, case = 72.0 }")
        self.assertEqual(doc[k[0].span()], "cpu")
        self.assertEqual(doc[k[1].span()], "case")
        self.assertEqual(doc[d["cpu"].span()], "79.5")
        self.assertEqual(doc[d["case"].span()], "72.0")

    def test_nested_dict(self):
        doc = """
              [bliibaa.diibaa]
              offsettime=[1979-05-27T00:32:00.999999-07:00]
              """
        toml = tomllib.loads(doc)

        first_key = list(toml.keys())[0]
        self.assertEqual(doc[first_key.span()], "bliibaa")
        first_level = toml["bliibaa"]

        self.assertEqual(first_level.span(), slice(0, 0), "Nested dict have no span")

        second_key = list(first_level.keys())[0]
        self.assertEqual(doc[second_key.span()], "diibaa")
        second_level = first_level["diibaa"]

        self.assertEqual(second_level.span(), slice(0, 0), "Nested dict have no span")

        third_key = list(second_level.keys())[0]
        self.assertEqual(doc[third_key.span()], "offsettime")
        array = second_level["offsettime"]

        self.assertEqual(doc[array.span()], "[1979-05-27T00:32:00.999999-07:00]")
        self.assertEqual(doc[array[0].span()], "1979-05-27T00:32:00.999999-07:00")

    def test_multiline(self):
        doc = r"""
re = '''\d{2} apps is t[wo]o many'''
lines = '''
The first newline is
trimmed in raw strings.
All other whitespace
is preserved.
'''
        """
        toml = tomllib.loads(doc)

        self.assertEqual(doc[toml["re"].span()], r"'''\d{2} apps is t[wo]o many'''")
        self.assertEqual(doc[toml["lines"].span()], """'''
The first newline is
trimmed in raw strings.
All other whitespace
is preserved.
'''""")

    def test_preserve_number_format(self):
        doc = """
        float1 = +1.0
        float2 = 3.1415
        float3 = -0.01
        float4 = 224_617.445_991_228

        infinite1 = inf # positive infinity
        infinite2 = +inf # positive infinity
        infinite3 = -inf # negative infinity
        """
        toml = tomllib.loads(doc)

        self.assertEqual(doc[toml["float1"].span()], "+1.0")
        self.assertEqual(doc[toml["float2"].span()], "3.1415")
        self.assertEqual(doc[toml["float3"].span()], "-0.01")
        self.assertEqual(doc[toml["float4"].span()], "224_617.445_991_228")

        self.assertEqual(doc[toml["infinite1"].span()], "inf")
        self.assertEqual(doc[toml["infinite2"].span()], "+inf")
        self.assertEqual(doc[toml["infinite3"].span()], "-inf")
