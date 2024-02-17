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
import matplotlib.pyplot as plt


def individual_rho(P_d_b, P_d_e, P_d_g, rho, sharey=True):
    """
    Plot P(d_hat=d) distribution for each rho value in individual subplot


    Parameters
    ----------
    P_d_b : np.ndarray
        mean(P(d_hat=d)) for each component using boostrap, of dimension (n_components, n_rho)

    P_d_e : np.ndarray
        P(d_hat=d) using eigenvalues, of dimension (n_components, n_rho)

    P_d_g : np.ndarray
        P(d_hat=d) using Gershgorin, of dimension (n_components, n_rho)

    rho : list or np.ndarray
        rho values corresponding to P_d, of len n_rho


    Returns
    -------
    None

    """

    # number of components
    nc = len(P_d_b)

    fig, axes = plt.subplots(figsize=(2 * nc, nc), nrows=1, ncols=nc, sharey=sharey)
    fig.suptitle(r'Distribution of $P(\widehat{d}_r=d_r)$')

    # Set the colors for each distribution
    colors = ['C0', 'C1', 'C2']
    colors_b = dict(color=colors[0])
    colors_e = dict(color=colors[1])
    colors_m = dict(color=colors[2])

    for idx in range(nc):
        axes[idx].boxplot(P_d_b[idx], positions=[1 + idx * 4],
                          boxprops=colors_b, medianprops=colors_b, whiskerprops=colors_b,
                          capprops=colors_b, flierprops=dict(markeredgecolor=colors[0]))

        axes[idx].boxplot(P_d_e[idx].flatten(), positions=[2 + idx * 4],
                          boxprops=colors_e, medianprops=colors_e, whiskerprops=colors_e,
                          capprops=colors_e, flierprops=dict(markeredgecolor=colors[1]))

        axes[idx].boxplot(P_d_g[idx], positions=[3 + idx * 4],
                          boxprops=colors_m, medianprops=colors_m, whiskerprops=colors_m,
                          capprops=colors_m, flierprops=dict(markeredgecolor=colors[2]))

        axes[idx].set_ylim([-0.05, 1.05])
        axes[idx].set_yticks([0, 0.5, 1])
        axes[idx].set_yticklabels(['$0.0$', '$0.5$', '$1.0$'])

        axes[idx].set_xticks([1 + idx * 4, 2 + idx * 4, 3 + idx * 4])
        axes[idx].set_xticklabels(['BT', 'EV', 'GD'], rotation=90)
        axes[idx].set_title(r'$\rho = ' + str(rho[idx]) + '$')
    axes[0].set_ylabel('$P(\widehat{d}_r = d_r)$')

    plt.tight_layout()
    plt.show()
