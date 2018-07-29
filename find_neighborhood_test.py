#! /usr/bin/env python

import find_neighborhood
import unittest


class StreetParseTest(unittest.TestCase):

  def assertStreetParsesTo(
      self, street_address, street_number, street_name, street_type):
    self.assertEquals(
      find_neighborhood.parse_street_address(street_address),
      (street_number, street_name, street_type))

  def test_basic_parse(self):
    self.assertStreetParsesTo("123 Main St", 123, "main", "st")

  def test_apt_number_parse(self):
    self.assertStreetParsesTo("123 Main St #101", 123, "main", "st")

  def test_street_type_normalization(self):
    self.assertStreetParsesTo("123 Main Street", 123, "main", "st")

  def test_street_type_normalization(self):
    self.assertStreetParsesTo("123 Main Street", 123, "main", "st")

  def test_apt_number_parse_with_suite(self):
    self.assertStreetParsesTo("123 Main St Suite101", 123, "main", "st")
    # Case not handled well, covered by tier3 prefix match
    self.assertStreetParsesTo("123 Main St Suite 101", 123, "main st suite", "")

  def test_street_type_missing(self):
    self.assertStreetParsesTo("123 Main", 123, "main", "")

  def test_number_with_letter_suffix(self):
    self.assertStreetParsesTo("123b Main St", 123, "main", "st")
    self.assertStreetParsesTo("123 Main St b", 123, "main", "st")

  def test_number_value_error(self):
    with self.assertRaises(ValueError):
      find_neighborhood.parse_street_address("b123 Main St")


class FindNeighborhoodTest(unittest.TestCase):

  def assertNeighborhood(self, street_address, neighborhood):
    self.assertEquals(
      find_neighborhood.find_neighborhood(
        "data/neighborhood_data.tsv.gz", street_address),
      neighborhood)

  def test_street_match(self):
    self.assertNeighborhood("123 Main St", "Financial District/South Beach") 

  def test_street_type_missing(self):
    self.assertNeighborhood("123 Main", "Financial District/South Beach")

  def test_junk_suffix(self):
    self.assertNeighborhood("123 Main Suite 100",
                            "Financial District/South Beach")

  def test_random_suffix(self):
    self.assertNeighborhood("123 Main Suite 100",
                            "Financial District/South Beach")

  def test_ambiguous_address(self):
    self.assertNeighborhood(
        "1 10th Apt 3",
        "Multiple matches: South of Market, Inner Richmond")

  def test_no_match(self):
    self.assertNeighborhood("1 asdf123 st", None)
  
  def test_empty_input(self):
    self.assertNeighborhood(" ", None)


if __name__ == '__main__':
    unittest.main()