from operator import itemgetter
import numpy as np
from sklearn.metrics import homogeneity_score, completeness_score, v_measure_score, silhouette_score, calinski_harabasz_score


class ModelQualityReporter(object):
    """
    - Reference: http://scikit-learn.org/stable/modules/clustering.html#clustering-evaluation

    This class is able to calculate scores based on different model evaluation metrics.
    Supported metrics are:

    * 'silhouette' for the Silhouette Coefficient in [-1, 1]: where a higher Silhouette Coefficient score relates to a model with better defined clusters.
        -- The score is bounded between -1 for incorrect clustering and +1 for highly dense clustering. Scores around zero indicate overlapping clusters.\n
        -- The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.
    * 'cali-hara' for the Calinski-Harabaz index in []: where a higher Calinski-Harabaz score relates to a model with better defined clusters.
        -- The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.\n
        -- The score is fast to compute
    """

    def __init__(self, strain_id2datapoint, strain_id2strainitem):
        self.strain_id2datapoint = strain_id2datapoint
        self.strain_id2strainitem = strain_id2strainitem
        self.methods = {
            'silhouette': silhouette_score,
            'cali-hara': calinski_harabasz_score
        }
        # needing ground truth labels
        self.dt_methods = {
            'homogeneity': homogeneity_score,
            'completeness': completeness_score,
            'v-measure': v_measure_score
        }
        self.clustering = None
        self.metric = ''
        self.score = None
        self.true_pred = None

    def __str__(self):
        return '\'{}\' on \'{}\' nb_clusters={} : {:.5f}'.format(self.metric, self.clustering.id, len(self.clustering), self.score)

    def measure(self, clustering, metric='silhouette'):
        """
        Calculates and returns an evaluation score based on the given metric on a Clustering.\n
        :param clustering: the Clustering object to evaluate
        :type clustering: clustering.Clustering
        :param metric: defines the evaluation formula/method
        :type metric: str
        :return: the calculated score
        :rtype: float
        """
        array = np.array([res for res in clustering.members_n_assigned_clusters()])
        arr1 = np.array([self.strain_id2datapoint[iid] for iid in array[:, 0]])
        self.clustering = clustering
        self.metric = metric
        self.score = self.methods[metric](arr1, array[:, 1])  # cluster ids act as 'predicted' labels
        return self

    def evaluate(self, clustering, metric='homogeneity'):
        """
        Evaluates using a metric that utilizes the ground truth (class labels) to compute the score.\n
        :param clustering:
        :param metric:
        :return:
        """
        strain_types = np.array([self.strain_id2strainitem[_id]['type'] for cl in clustering for _id in cl])
        pred_labels = [[get_cluster_label(cl, 'type')] * len(cl) for cl in clustering]
        pred_labels = [item for sublist in pred_labels for item in sublist]
        self.clustering = clustering
        self.metric = metric
        su = sum(map(lambda x: 1 if strain_types[x] == pred_labels[x] else 0, [i for i in range(len(strain_types))]))
        # print('{} {} {}'.format(i, j, r))
        # print('SUM: {}'.format(su))
        self.score = self.dt_methods[metric](strain_types, pred_labels)
        self.true_pred = (su, len(strain_types))
        return self

# def get_model_quality_reporter(strain_dataset_id):
#     if strain_dataset_id not in cls_evals:
#         cls_evals[strain_dataset_id] = ModelQualityReporter(strain_master[strain_dataset_id].dt.id2datapoint, strain_master[strain_dataset_id].dt.full_df.loc)
#     return cls_evals[strain_dataset_id]

# holds a ModelQualityreporter per dataset id
cls_evals = {}


def get_model_quality_reporter(strain_master, strain_dataset_id):
    if strain_dataset_id not in cls_evals:
        cls_evals[strain_dataset_id] = ModelQualityReporter(strain_master[strain_dataset_id].dt.id2datapoint, strain_master[strain_dataset_id].dt.full_df.loc)
    return cls_evals[strain_dataset_id]


def get_cluster_label(cluster, variable):
    return max(cluster.freqs[variable].items(), key=itemgetter(1))[0]
