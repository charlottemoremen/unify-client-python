from unittest import TestCase

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.attribute_configuration.resource import (
    AttributeConfiguration,
)


class TestAttributeConfigurations(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("admin", "dt")
        self.unify = Client(auth, host="10.10.0.90")

    def test_resource(self):
        alias = "projects/1/attributeConfigurations/26"
        test = AttributeConfiguration(self.unify, self.AC_json[0], alias)

        expected = alias
        self.assertEqual(expected, test.relative_id)

        expected = self.AC_json[0]["id"]
        self.assertEqual(expected, test.id)

        expected = self.AC_json[0]["relativeAttributeId"]
        self.assertEqual(expected, test.relativeAttributeId)

        expected = self.AC_json[0]["attributeRole"]
        self.assertEqual(expected, test.attributeRole)

        expected = self.AC_json[0]["similarityFunction"]
        self.assertEqual(expected, test.similarityFunction)

        expected = self.AC_json[0]["enabledForMl"]
        self.assertEqual(expected, test.enabledForMl)

        expected = self.AC_json[0]["tokenizer"]
        self.assertEqual(expected, test.tokenizer)

        expected = self.AC_json[0]["numericFieldResolution"]
        self.assertEqual(expected, test.numericFieldResolution)

        expected = self.AC_json[0]["attributeName"]
        self.assertEqual(expected, test.attributeName)

    def test_resource_from_json(self):
        alias = "projects/1/attributeConfigurations/26"
        expected = AttributeConfiguration(self.unify, self.AC_json[0], alias)
        actual = AttributeConfiguration.from_json(self.unify, self.AC_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    AC_json = [
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/26",
            "relativeId": "projects/1/attributeConfigurations/26",
            "relativeAttributeId": "datasets/8/attributes/surname",
            "attributeRole": "CLUSTER_NAME_ATTRIBUTE",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "surname",
        }
    ]
