from unittest import TestCase
from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from dnz_client import get_client


class TestClient(TestCase):

    def setUp(self):
        self.mock_strategy = Mock(spec=BaseRequestStrategy)
        self.client = get_client(request_strategy=self.mock_strategy)

    def test_format_dict_param(self):
        values = {
            "collection": "Music 101",
            "subject": ["Cats", "Weddings"],
        }
        filter_type = "and"
        expected = {
            "and[collection][]": "Music 101",
            "and[subject][]": ["Cats", "Weddings"],
        }
        actual = self.client._format_dict_param(filter_type, values)
        self.assertEqual(expected, actual)

    def test_format_multivalue_param(self):
        values = ["a", "b", "c"]
        expected = "a,b,c"
        actual = self.client._format_multivalue_param(values)
        self.assertEqual(expected, actual)

    def test_format_multivalue_param_empty(self):
        values = []
        expected = None
        actual = self.client._format_multivalue_param(values)
        self.assertEqual(expected, actual)

    def test_generate_metadata_params(self):
        fields = ["id", "title"]
        expected = {"fields": "id,title"}
        actual = self.client._generate_metadata_params(fields)
        self.assertEqual(expected, actual)

    def test_generate_search_params(self):
        data = {
            "direction": "desc",
            "exclude_filters_from_facets": "true",
            "facets_page": "2",
            "page": "3",
            "per_page": "10",
            "sort": "date",
            "text": "moustache",
            "facets": ["collection", "creator"],
            "fields": ["id", "title", "subject"],
            "geo_bbox": ["-41", "174", "-42", "175"],
            "_and": {
                "has_lat_lng": "true",
                "subject": ["Cats", "Weddings"],
                "year": "[1982 TO 1987]",
            },
            "_or": {"category": ["Audio", "Videos"]},
            "_without": {"primary_collection": "Papers Past"},
        }
        expected = {
            "direction": "desc",
            "exclude_filters_from_facets": "true",
            "facets_page": "2",
            "page": "3",
            "per_page": "10",
            "sort": "date",
            "text": "moustache",
            "facets": "collection,creator",
            "fields": "id,title,subject",
            "geo_bbox": "-41,174,-42,175",
            "and[has_lat_lng]": "true",
            "and[subject][]": ["Cats", "Weddings"],
            "and[year]": "[1982 TO 1987]",
            "and[or][category][]": ["Audio", "Videos"],
            "without[primary_collection][]": "Papers Past",
        }
        actual = self.client._generate_search_params(**data)
        self.assertEqual(expected, actual)

    def test_metadata(self):
        fields = ["id", "title"]
        record_id = 132
        self.client.metadata(record_id, fields)
        self.mock_strategy.get.assert_called_with(
            "http://api.digitalnz.org/v3/records/132.json",
            params={"fields": "id,title"})

    def test_search(self):
        data = {
            "text": "moustache",
            "facets": ["collection", "creator"],
            "_and": {
                "subject": ["Cats", "Weddings"],
                "year": "[1982 TO 1987]",
            },
            "_or": {"category": ["Audio", "Videos"]},
        }
        params = {
            "text": "moustache",
            "facets": "collection,creator",
            "and[subject][]": ["Cats", "Weddings"],
            "and[year]": "[1982 TO 1987]",
            "and[or][category][]": ["Audio", "Videos"],
        }
        self.client.search(**data)
        self.mock_strategy.get.assert_called_with(
            "http://api.digitalnz.org/v3/records.json",
            params=params)
