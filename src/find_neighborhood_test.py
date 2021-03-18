#! /usr/bin/env python

import find_neighborhood
import pytest


def assert_parse(street_address, street_number, street_name, street_type):
    assert find_neighborhood.parse_street_address(street_address) == (
        street_number,
        street_name,
        street_type,
    )


def test_basic_parse():
    assert_parse("123 Main St", 123, "main", "st")


def test_apt_number_parse():
    assert_parse("123 Main St #101", 123, "main", "st")


def test_street_type_normalization():
    assert_parse("123 Main Street", 123, "main", "st")


def test_street_type_normalization():
    assert_parse("123 Main Street", 123, "main", "st")


def test_apt_number_parse_with_suite():
    assert_parse("123 Main St Suite 101", 123, "main", "st")


def test_street_type_missing():
    assert_parse("123 Main", 123, "main", "")


def test_number_with_letter_suffix():
    assert_parse("123b Main St", 123, "main", "st")
    assert_parse("123 Main St b", 123, "main", "st")


def test_number_value_error():
    with pytest.raises(ValueError):
        find_neighborhood.parse_street_address("b123 Main St")


def test_empty_error():
    with pytest.raises(ValueError):
        find_neighborhood.parse_street_address("")
    with pytest.raises(ValueError):
        find_neighborhood.parse_street_address(None)


def assert_find_results(street_address, district, neighborhood):
    assert find_neighborhood.db.find(street_address) == {
        "district": district.split(",") if district else [],
        "neighborhood": neighborhood.split(",") if neighborhood else [],
    }


def test_street_match():
    assert_find_results("123 Main St", "6", "Financial District/South Beach")


def test_padded_street_match():
    assert_find_results("   123 Main St   ", "6", "Financial District/South Beach")


def test_full_address():
    assert_find_results(
        "123 Main St, San Francisco, CA 94105",
        "6",
        "Financial District/South Beach",
    )


def test_street_type_missing():
    assert_find_results("123 Main", "6", "Financial District/South Beach")


def test_junk_suffix():
    assert_find_results("123 Main Suite 100", "6", "Financial District/South Beach")


def test_random_suffix():
    assert_find_results("123 Main Suite 100", "6", "Financial District/South Beach")


def test_unparseable_address():
    assert_find_results("1 10th", "", "")
    assert_find_results("1 10th Apt 3", "", "")
    assert_find_results("b123 Main St", "", "")


def test_ambiguous_address():
    assert_find_results("10 10th Apt 3", "2,6", "Inner Richmond,South of Market")


def test_no_match():
    assert_find_results("1 asdf123 st", "", "")


def test_empty_input():
    assert_find_results(" ", "", "")
    assert_find_results(None, "", "")
