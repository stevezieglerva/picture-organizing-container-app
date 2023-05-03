import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from uuid import uuid1

from infrastructure.repository.DynamoDB import DynamoDB


class Query(unittest.TestCase):
    def test_should_basic_pk_sk_lookup(self):
        # Arrange
        subject = DynamoDB("master-pictures-catalog-test")

        # Act
        results = subject.query_table_equal(
            {"gsi2_pk": "STATE", "gsi2_sk": "NC"}, "gsi2"
        )
        print(f"test results: {results}")

        # Assert
        self.assertGreaterEqual(len(results), 0)


class BatchOperations(unittest.TestCase):
    def test_should_put_items_in_batch(self):
        # Arrange
        subject = DynamoDB("master-pictures-catalog-test")
        input = [
            {"pk": "INTEGRATION_TEST", "sk": str(uuid1()), "name": "joe"},
            {"pk": "INTEGRATION_TEST", "sk": str(uuid1()), "name": "jane"},
            {"pk": "INTEGRATION_TEST", "sk": str(uuid1()), "name": "jack"},
        ]

        # Act
        results = subject.put_batch(input, 2)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.batches_sent, 2)
        self.assertEqual(results.batch_results[0]["UnprocessedItems"], {})

    def test_should_delete_items_in_one_batch(self):
        # Arrange
        subject = DynamoDB("master-pictures-catalog-test")
        input = [
            {"pk": "INTEGRATION_TEST", "sk": "a", "name": "joe"},
            {"pk": "INTEGRATION_TEST", "sk": "b", "name": "jane"},
        ]
        results = subject.put_batch(input)
        input = [
            {"pk": "INTEGRATION_TEST", "sk": "a"},
            {"pk": "INTEGRATION_TEST", "sk": "b"},
        ]

        # Act
        print(f"test results: {results}")
        results = subject.delete_batch(input)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.batches_sent, 1)
        self.assertEqual(results.batch_results[0]["UnprocessedItems"], {})

    def test_should_delete_items_in_multiple_batches(self):
        # Arrange
        subject = DynamoDB("master-pictures-catalog-test")
        input = [
            {"pk": "INTEGRATION_TEST", "sk": "a", "name": "joe"},
            {"pk": "INTEGRATION_TEST", "sk": "b", "name": "jane"},
        ]
        results = subject.put_batch(input, 1)
        input = [
            {"pk": "INTEGRATION_TEST", "sk": "a"},
            {"pk": "INTEGRATION_TEST", "sk": "b"},
        ]

        # Act
        print(f"test results: {results}")
        results = subject.delete_batch(input, 1)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.batches_sent, 2)
        self.assertEqual(results.batch_results[0]["UnprocessedItems"], {})
        self.assertEqual(results.batch_results[1]["UnprocessedItems"], {})


if __name__ == "__main__":
    unittest.main()
