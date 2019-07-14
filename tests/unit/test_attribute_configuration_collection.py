from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.attribute_configuration.collection import (
    AttributeConfigurationCollection,
)


class TestAttributeConfigurationsCollection(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_relative(self):
        AC_url = f"http://localhost:9100/api/versioned/v1/projects/1/attributeConfigurations/1"
        alias = "projects/1/attributeConfigurations/"
        AC_test = AttributeConfigurationCollection(self.unify, self.ACC_json[0], alias)
        expected = self.ACC_json[0]
        responses.add(responses.GET, AC_url, json=self.ACC_json[0])
        self.assertEqual(
            expected["relativeId"],
            AC_test.by_relative_id("projects/1/attributeConfigurations/1").relative_id,
        )

    @responses.activate
    def test_resource(self):
        AC_url = f"http://localhost:9100/api/versioned/v1/projects/1/attributeConfigurations/1"
        alias = "projects/1/attributeConfigurations/"
        AC_test = AttributeConfigurationCollection(self.unify, self.ACC_json[0], alias)
        expected = self.ACC_json[0]
        responses.add(responses.GET, AC_url, json=self.ACC_json[0])
        self.assertEqual(
            expected["relativeId"], AC_test.by_resource_id("1").relative_id
        )

    @responses.activate
    def test_create(self):
        create_json = [
            {
                "id": "unify://unified-data/v1/projects/1/attributeConfigurations/35",
                "relativeId": "projects/1/attributeConfigurations/35",
                "relativeAttributeId": "datasets/79/attributes/Tester",
                "attributeRole": "",
                "similarityFunction": "ABSOLUTE_DIFF",
                "enabledForMl": False,
                "tokenizer": "",
                "numericFieldResolution": [],
                "attributeName": "Tester",
            }
        ]

        project_json = [
            {
                "id": "unify://unified-data/v1/projects/1",
                "externalId": "project 1 external ID",
                "name": "project 1 name",
                "description": "project 1 description",
                "type": "DEDUP",
                "unifiedDatasetName": "project 1 unified dataset",
                "created": {
                    "username": "admin",
                    "time": "2018-09-10T16:06:20.636Z",
                    "version": "project 1 created version",
                },
                "lastModified": {
                    "username": "admin",
                    "time": "2018-09-10T16:06:20.851Z",
                    "version": "project 1 modified version",
                },
                "relativeId": "projects/1",
            }
        ]

        url = (
            f"http://localhost:9100/api/versioned/v1/projects/1/attributeConfigurations"
        )
        project_url = f"http://localhost:9100/api/versioned/v1/projects/1"
        responses.add(responses.GET, project_url, json=project_json[0])
        responses.add(responses.GET, url, json={})
        responses.add(responses.POST, url, json=create_json[0], status=204)
        responses.add(responses.GET, url, json=create_json)

        attributeconfig = (
            self.unify.projects.by_resource_id("1")
            .as_mastering()
            .attribute_configurations()
        )
        create = attributeconfig.create(create_json)

        assert create.relative_id == create_json[0]["relativeId"]

    ACC_json = [
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/1",
            "relativeId": "projects/1/attributeConfigurations/1",
            "relativeAttributeId": "datasets/8/attributes/suburb",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "suburb",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/2",
            "relativeId": "projects/1/attributeConfigurations/2",
            "relativeAttributeId": "datasets/8/attributes/sex",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "sex",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/3",
            "relativeId": "projects/1/attributeConfigurations/3",
            "relativeAttributeId": "datasets/8/attributes/address_2",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "address_2",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/4",
            "relativeId": "projects/1/attributeConfigurations/4",
            "relativeAttributeId": "datasets/8/attributes/age",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "age",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/5",
            "relativeId": "projects/1/attributeConfigurations/5",
            "relativeAttributeId": "datasets/8/attributes/culture",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "culture",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/6",
            "relativeId": "projects/1/attributeConfigurations/6",
            "relativeAttributeId": "datasets/8/attributes/street_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "street_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/7",
            "relativeId": "projects/1/attributeConfigurations/7",
            "relativeAttributeId": "datasets/8/attributes/postcode",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "postcode",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/8",
            "relativeId": "projects/1/attributeConfigurations/8",
            "relativeAttributeId": "datasets/8/attributes/phone_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "phone_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/9",
            "relativeId": "projects/1/attributeConfigurations/9",
            "relativeAttributeId": "datasets/8/attributes/soc_sec_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "soc_sec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/10",
            "relativeId": "projects/1/attributeConfigurations/10",
            "relativeAttributeId": "datasets/8/attributes/rec2_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "rec2_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/11",
            "relativeId": "projects/1/attributeConfigurations/11",
            "relativeAttributeId": "datasets/8/attributes/date_of_birth",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "date_of_birth",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/12",
            "relativeId": "projects/1/attributeConfigurations/12",
            "relativeAttributeId": "datasets/8/attributes/title",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "title",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/13",
            "relativeId": "projects/1/attributeConfigurations/13",
            "relativeAttributeId": "datasets/8/attributes/address_1",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "address_1",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/14",
            "relativeId": "projects/1/attributeConfigurations/14",
            "relativeAttributeId": "datasets/8/attributes/rec_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "rec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/15",
            "relativeId": "projects/1/attributeConfigurations/15",
            "relativeAttributeId": "datasets/8/attributes/state",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "state",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/16",
            "relativeId": "projects/1/attributeConfigurations/16",
            "relativeAttributeId": "datasets/8/attributes/family_role",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "family_role",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/17",
            "relativeId": "projects/1/attributeConfigurations/17",
            "relativeAttributeId": "datasets/8/attributes/blocking_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "blocking_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/18",
            "relativeId": "projects/1/attributeConfigurations/18",
            "relativeAttributeId": "datasets/8/attributes/surname",
            "attributeRole": "CLUSTER_NAME_ATTRIBUTE",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "surname",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/19",
            "relativeId": "projects/1/attributeConfigurations/19",
            "relativeAttributeId": "datasets/8/attributes/given_name",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "given_name",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/20",
            "relativeId": "projects/1/attributeConfigurations/20",
            "relativeAttributeId": "datasets/8/attributes/Address1",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": False,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "Address1",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/21",
            "relativeId": "projects/1/attributeConfigurations/21",
            "relativeAttributeId": "datasets/8/attributes/Address2",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": False,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "Address2",
        },
    ]

    Acc_Json2 = [
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/1",
            "relativeId": "projects/1/attributeConfigurations/1",
            "relativeAttributeId": "datasets/8/attributes/suburb",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "suburb",
        }
    ]