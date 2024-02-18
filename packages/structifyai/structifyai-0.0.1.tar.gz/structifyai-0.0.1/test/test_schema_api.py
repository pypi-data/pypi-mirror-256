# coding: utf-8

"""
    Structify

    Structify's goal is to take every source of knowledge and represent it on one place, deduplicated in the format that you specify.

    Version: 0.1.0

    Contact: team@structify.ai
"""


import unittest

from structifyai.api.schema_api import SchemaApi  # noqa: E501


class TestSchemaApi(unittest.TestCase):
    """SchemaApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SchemaApi()  # noqa: E501

    def tearDown(self) -> None:
        pass

    def test_create(self) -> None:
        """Test case for create

        Create a new schema  # noqa: E501
        """
        pass

    def test_get(self) -> None:
        """Test case for get

        Gets information about a schema  # noqa: E501
        """
        pass

    def test_list(self) -> None:
        """Test case for list

        Lists Schemas  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
