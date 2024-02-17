#     Copyright (c) <2024> <University of Paderborn>
#     Signal and System Theory Group, Univ. of Paderborn, https://sst-group.org/
#     https://github.com/SSTGroup/relationship_structure_identification
#
#     Permission is hereby granted, free of charge, to any person
#     obtaining a copy of this software and associated documentation
#     files (the "Software"), to deal in the Software without restriction,
#     including without limitation the rights to use, copy, modify and
#     merge the Software, subject to the following conditions:
#
#     1.) The Software is used for non-commercial research and
#        education purposes.
#
#     2.) The above copyright notice and this permission notice shall be
#        included in all copies or substantial portions of the Software.
#
#     3.) Publication, Distribution, Sublicensing, and/or Selling of
#        copies or parts of the Software requires special agreements
#        with the University of Paderborn and is in general not permitted.
#
#     4.) Modifications or contributions to the software must be
#        published under this license. The University of Paderborn
#        is granted the non-exclusive right to publish modifications
#        or contributions in future versions of the Software free of charge.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#     OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#     NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#     HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#     WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#     OTHER DEALINGS IN THE SOFTWARE.
#
#     Persons using the Software are encouraged to notify the
#     Signal and System Theory Group at the University of Paderborn
#     about bugs. Please reference the Software in your publications
#     if it was used for them.


import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt


def detect_number_blocks_using_bootstrap(sources, B, P_fa):
    # estimate number of eigenvalues greater than 1 in each SCV
    # sources with dimensions n_samples x n_datasets

    T, K = sources.shape

    # make sources zero-mean and unit-variance
    standardized_sources = sources - np.mean(sources, axis=0)
    standardized_sources /= np.std(standardized_sources, axis=0)

    C = np.abs(1 / T * standardized_sources.T @ standardized_sources)  # shape K x K
    eig_val, _ = np.linalg.eigh(C)

    # sort eigenvalues in descending order
    test_val = eig_val[:: -1]

    # resample indices with replacement and calculate test_val for each resampled cov
    test_val_b = np.zeros((K, B))
    for b in range(B):
        j = np.random.randint(0, T, T)
        S_b = standardized_sources[j, :]
        # S_b /= np.std(S_b, axis=0)  # we do not normalize again because d_hat will then more often be overestimated
        C_b = np.abs(1 / T * S_b.T @ S_b)
        eig_val_b, _ = np.linalg.eigh(C_b)
        test_val_b[:, b] = eig_val_b[:: -1]

    # vector epsilon: 1 means the kth eigenvalue is greater than 1, 0 means less or equal.
    epsilon = np.ones(K)
    for k in range(K):
        test_statistic = test_val[k] - 1
        test_star_b = np.zeros(B)
        for b in range(B):
            test_star_b[b] = test_val_b[k, b] - test_val[k]
        # sort test_start_b
        test_star_b = np.sort(test_star_b)  # should be ascending
        eta = (np.floor((1 - P_fa) * (B + 1))).astype(int)
        test_tau = test_star_b[eta - 1]  # Python indexing starts at 0
        if test_statistic < test_tau:  # means that eigenvalue element is less than or equal to 1
            epsilon[k] = 0

    n_subblocks = np.count_nonzero(epsilon)
    return n_subblocks


def detect_number_blocks_using_direct_eigval(sources):
    # estimate number of eigenvalues greater than 1 in each SCV
    # sources with dimensions n_samples x n_datasets

    # make sources zero-mean and unit-variance
    standardized_sources = sources - np.mean(sources, axis=0)
    standardized_sources /= np.std(standardized_sources, axis=0)

    C = np.abs(1 / standardized_sources.shape[0] * standardized_sources.T @ standardized_sources)  # shape K x K
    eig_val, _ = np.linalg.eigh(C)

    # compare directly with 1
    n_subblocks = np.count_nonzero(eig_val > 1)
    return n_subblocks


def detect_number_blocks_using_gershgorin(sources):
    # Gershgorin discs from Hanlu's ICASSP paper
    # estimate number of eigenvalues greater than 1 in each SCV
    # sources with dimensions n_samples x n_datasets

    # make sources zero-mean and unit-variance
    standardized_sources = sources - np.mean(sources, axis=0)
    standardized_sources /= np.std(standardized_sources, axis=0)

    C = np.abs(1 / standardized_sources.shape[0] * standardized_sources.T @ standardized_sources)  # shape K x K

    # calculate radius = sum of off-diagonal elements in ith row
    radius = np.zeros(C.shape[1])

    for i in range(C.shape[1]):
        radius[i] = np.sum(np.abs(C[i, :])) - np.abs(C[i, i])

    # if all elements in radius are 0 --> diagonal matrix. Then set Rmin to infinity because no grouping is there
    if np.linalg.norm(radius) == 0:
        Rmin = np.inf
    else:
        # minimum non-zero radius
        Rmin = np.min(radius[np.nonzero(radius)[0]])

    eig_val, _ = np.linalg.eigh(C)

    # number of groupings
    n_groupings = 0
    for lambda_i in eig_val:
        if lambda_i > Rmin + 1 + 1e-10:  # correction for machine error
            n_groupings += 1

    return n_groupings


def cluster_datasets(sources, n_clusters, B, P_fa, labels=None, plot=True):
    # cluster tasks based on non-common SCVs
    # S: np.ndarray of dimensions n_components x n_observations x n_datasets

    n_c, T, K = sources.shape
    n_subblocks = np.zeros(n_c, dtype=int)
    for idx in range(n_c):
        n_subblocks[idx] = detect_number_blocks_using_bootstrap(sources[idx, :, :], B, P_fa)

    structured_idx = n_subblocks > 1
    structured_sources = sources[structured_idx, :, :]
    structured_subblocks = n_subblocks[structured_idx]
    n_s = structured_subblocks.shape[0]

    # make sources zero-mean and unit-variance
    standardized_sources = structured_sources - np.mean(structured_sources, axis=0)
    standardized_sources /= np.std(standardized_sources, axis=0)

    # store d eigenvectors of each structured SCV in classify_vectors
    classify_vectors = []
    for scv_idx in range(n_s):
        S_temp = standardized_sources[scv_idx, :, :]
        C = np.abs(1 / T * S_temp.T @ S_temp)  # shape K x K
        _, eig_vec = np.linalg.eigh(C)

        eig_vecs = eig_vec[:, -structured_subblocks[scv_idx]:]
        classify_vectors.append(eig_vecs)

    if labels is None:
        labels = ['AOD-N', 'AOD-NS', 'AOD-T', 'AOD-TS', 'SM',
                  'SIRP-E1', 'SIRP-E3', 'SIRP-E5',
                  'SIRP-P1', 'SIRP-P3', 'SIRP-P5']

    if len(classify_vectors) != 0:
        # concatenate all eigenvectors in feature matrix
        feature_vectors = np.hstack(classify_vectors)

        if plot:
            # perform hierarchical/agglomerative clustering visually
            # use 'ward', which is also used in AgglomerativeClustering
            linked = linkage(feature_vectors, 'ward')
            plt.figure()
            dendrogram(linked,
                       orientation='top',
                       labels=labels,
                       leaf_rotation=90,
                       distance_sort='descending')
            plt.tight_layout()
            plt.xlabel('Dataset label')
            plt.ylabel('Distance')
            plt.show()

        # use hierarchical/agglomerative clustering to calculate labels. 'ward' is default anyway
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        model = model.fit(feature_vectors)
        cluster_labels = model.labels_
    else:
        cluster_labels = np.ones(K)

    return cluster_labels
