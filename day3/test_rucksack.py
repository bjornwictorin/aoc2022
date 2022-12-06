#!/usr/bin/env python3

import rucksack as rs


def test_get_item_value():
    item = "a"
    value = rs.get_item_value(item)
    assert value == 1
    item = "z"
    value = rs.get_item_value(item)
    assert value == 26
    item = "A"
    value = rs.get_item_value(item)
    assert value == 27
    item = "Z"
    value = rs.get_item_value(item)
    assert value == 52
