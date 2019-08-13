import json

from tamr_unify_client.base_model import MachineLearningModel
from tamr_unify_client.dataset.resource import Dataset
from tamr_unify_client.mastering.binning_model import BinningModel
from tamr_unify_client.mastering.estimated_pair_counts import EstimatedPairCounts
from tamr_unify_client.mastering.published_cluster.configuration import (
    PublishedClustersConfiguration,
)
from tamr_unify_client.mastering.published_cluster.record import RecordPublishedCluster
from tamr_unify_client.mastering.published_cluster.resource import PublishedCluster
from tamr_unify_client.project.resource import Project


class MasteringProject(Project):
    """A Mastering project in Tamr."""

    def pairs(self):
        """Record pairs generated by Tamr's binning model.
        Pairs are displayed on the "Pairs" page in the Tamr UI.

        Call :func:`~tamr_unify_client.dataset.resource.Dataset.refresh` from
        this dataset to regenerate pairs according to the latest binning model.

        :returns: The record pairs represented as a dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        alias = self.api_path + "/recordPairs"
        return Dataset(self.client, None, alias)

    def pair_matching_model(self):
        """Machine learning model for pair-matching for this Mastering project.
        Learns from verified labels and predicts categorization labels for unlabeled pairs.

        Calling :func:`~tamr_unify_client.base_model.MachineLearningModel.predict`
        from this dataset will produce new (unpublished) clusters. These clusters
        are displayed on the "Clusters" page in the Tamr UI.

        :returns: The machine learning model for pair-matching.
        :rtype: :class:`~tamr_unify_client.base_model.MachineLearningModel`
        """
        alias = self.api_path + "/recordPairsWithPredictions/model"
        return MachineLearningModel(self.client, None, alias)

    def high_impact_pairs(self):
        """High-impact pairs as a dataset. Tamr labels pairs as "high-impact" if
        labeling these pairs would help it learn most quickly (i.e. "Active learning").

        High-impact pairs are displayed with a ⚡ lightning bolt icon on the
        "Pairs" page in the Tamr UI.

        Call :func:`~tamr_unify_client.dataset.resource.Dataset.refresh` from
        this dataset to produce new high-impact pairs according to the latest
        pair-matching model.

        :returns: The high-impact pairs represented as a dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        alias = self.api_path + "/highImpactPairs"
        return Dataset(self.client, None, alias)

    def record_clusters(self):
        """Record Clusters as a dataset. Tamr clusters labeled pairs using pairs
        model. These clusters populate the cluster review page and get transient
        cluster ids, rather than published cluster ids (i.e., "Permanent Ids")

        Call :func:`~tamr_unify_client.dataset.resource.Dataset.refresh` from
        this dataset to generate clusters based on to the latest pair-matching model.

        :returns: The record clusters represented as a dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        alias = self.api_path + "/recordClusters"
        return Dataset(self.client, None, alias)

    def published_clusters(self):
        """Published record clusters generated by Tamr's pair-matching model.

        :returns: The published clusters represented as a dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """

        unified_dataset = self.unified_dataset()

        # Replace this workaround with a direct API call once API
        # is fixed. APIs that need to work are: fetching the dataset and
        # being able to call refresh on resulting dataset. Until then, we grab
        # the dataset by constructing its name from the corresponding Unified Dataset's name
        name = unified_dataset.name + "_dedup_published_clusters"
        canonical = self.client.datasets.by_name(name)
        resource_json = canonical._data
        alias = self.api_path + "/publishedClusters"
        return Dataset.from_json(self.client, resource_json, alias)

    def published_clusters_configuration(self):
        """Retrieves published clusters configuration for this project.

        :returns: The published clusters configuration
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfiguration`
        """
        alias = self.api_path + "/publishedClustersConfiguration"
        resource_json = self.client.get(alias).successful().json()
        return PublishedClustersConfiguration.from_json(
            self.client, resource_json, alias
        )

    def published_cluster_ids(self):
        """Retrieves published cluster IDs for this project.

        :returns: The published cluster ID dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        # Replace this workaround with a direct API call once API
        # is fixed. APIs that need to work are: fetching the dataset and
        # being able to call refresh on resulting dataset. Until then, we grab
        # the dataset by constructing its name from the corresponding Unified Dataset's name
        unified_dataset = self.unified_dataset()
        name = unified_dataset.name + "_dedup_all_persistent_ids"
        dataset = self.client.datasets.by_name(name)

        path = self.api_path + "/allPublishedClusterIds"
        return Dataset.from_json(self.client, dataset._data, path)

    def published_cluster_stats(self):
        """Retrieves published cluster stats for this project.

        :returns: The published cluster stats dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        # Replace this workaround with a direct API call once API
        # is fixed. APIs that need to work are: fetching the dataset and
        # being able to call refresh on resulting dataset. Until then, we grab
        # the dataset by constructing its name from the corresponding Unified Dataset's name
        unified_dataset = self.unified_dataset()
        name = unified_dataset.name + "_dedup_published_cluster_stats"
        dataset = self.client.datasets.by_name(name)

        path = self.api_path + "/publishedClusterStats"
        return Dataset.from_json(self.client, dataset._data, path)

    def published_cluster_versions(self, cluster_ids):
        """Retrieves version information for the specified published clusters.
        See https://docs.tamr.com/reference#retrieve-published-clusters-given-cluster-ids.

        :param cluster_ids: The persistent IDs of the clusters to get version information for.
        :type cluster_ids: iterable[str]
        :return: A stream of the published clusters.
        :rtype: Python generator yielding :class:`~tamr_unify_client.mastering.published_cluster.resource.PublishedCluster`
        """
        path = self.api_path + "/publishedClusterVersions"
        return self._cluster_versions(PublishedCluster, cluster_ids, path)

    def record_published_cluster_versions(self, record_ids):
        """Retrieves version information for the published clusters of the given records.
        See https://docs.tamr.com/reference#retrieve-published-clusters-given-record-ids.

        :param record_ids: The Tamr IDs of the records to get cluster version information for.
        :type record_ids: iterable[str]
        :return: A stream of the relevant published clusters.
        :rtype: Python generator yielding :class:`~tamr_unify_client.mastering.published_cluster.record.RecordPublishedCluster`
        """
        path = self.api_path + "/recordPublishedClusterVersions"
        return self._cluster_versions(RecordPublishedCluster, record_ids, path)

    def _cluster_versions(self, cluster_class, ids, endpoint):
        """Retrieves version information for published clusters.

        :param cluster_class: The class to create instances of.
        :param ids: The IDs of the clusters or records to get version information for.
        :type ids: iterable[str]
        :param endpoint: The endpoint to call for versions.
        :type endpoint: str
        :return: A stream of the published clusters.
        """
        string_ids = "\n".join(json.dumps(i) for i in ids)

        with self.client.post(endpoint, data=string_ids, stream=True) as response:
            for line in response.iter_lines():
                yield cluster_class(json.loads(line))

    def estimate_pairs(self):
        """Returns pair estimate information for a mastering project

        :return: Pairs Estimate information.
        :rtype: :class:`~tamr_unify_client.mastering.estimated_pair_counts.EstimatedPairCounts`
        """
        alias = self.api_path + "/estimatedPairCounts"
        estimate_json = self.client.get(alias).successful().json()
        info = EstimatedPairCounts.from_json(self.client, estimate_json, api_path=alias)
        return info

    def record_clusters_with_data(self):
        """Project's unified dataset with associated clusters.

        :returns: The record clusters with data represented as a dataset
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        unified_dataset = self.unified_dataset()

        # Replace this workaround with a direct API call once API
        # is fixed. APIs that need to work are: fetching the dataset and
        # being able to call refresh on resulting dataset. Until then, we grab
        # the dataset by constructing its name from the corresponding Unified Dataset's name
        name = unified_dataset.name + "_dedup_clusters_with_data"
        return self.client.datasets.by_name(name)

        # super.__repr__ is sufficient

    def published_clusters_with_data(self):
        """Project's unified dataset with associated clusters.

        :returns: The published clusters with data represented as a dataset
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """

        unified_dataset = self.unified_dataset()
        name = unified_dataset.name + "_dedup_published_clusters_with_data"
        return self.client.datasets.by_name(name)

    def binning_model(self):
        """
        Binning model for this project.

        :return: Binning model for this project.
        :rtype: :class:`~tamr_unify_client.mastering.binning_model.BinningModel`
        """
        alias = self.api_path + "/binningModel"

        # Cannot get this resource and so we hard code
        resource_json = {"relativeId": alias}
        return BinningModel.from_json(self.client, resource_json, alias)
