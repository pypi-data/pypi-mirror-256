import unittest
from unittest.mock import patch
from tests.mocks import mock_imports


@patch.dict('os.environ', {'AzureSql_Server': 'test_server',
                           'AzureSql_Database': 'test_database'})
class TestDatabase(unittest.TestCase):
    @mock_imports()
    def get_database(self):
        from src.azuretoolbox.database import Database
        return Database()

    def test_database_connection_returns_true(self):
        # Arrange
        db = self.get_database()

        # Act
        result = db.connect('test_server', 'test_database',
                            'test_user', 'test_password')

        # Assert
        self.assertTrue(result)

    def test_database_disconnection_returns_true_when_connection_is_not_open(self):
        # Arrange
        db = self.get_database()

        # Act
        result = db.disconnect()

        # Assert
        self.assertTrue(result)

    def test_database_disconnection_returns_true_when_connection_is_open(self):
        # Arrange
        db = self.get_database()
        db.connect('test_server', 'test_database',
                   'test_user', 'test_password')

        # Act
        result = db.disconnect()

        # Assert
        self.assertTrue(result)

    def test_database_query_returns_expected_values(self):
        # Arrange
        db = self.get_database()
        db.connect('test_server', 'test_database',
                   'test_user', 'test_password')

        # Act & Assert
        self.assertIsNotNone(db.query('SELECT 1'))

    def test_parsing_response_returns_expected_values(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test')]
        header = [('id', None), ('name', None)]

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(result, [{'id': 1, 'name': 'test'}])


if __name__ == '__main__':
    unittest.main()
