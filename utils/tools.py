import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from algorithm.base import Algorithm
from algorithm.naive import BruteForce
from algorithm.rabin_karp import RabinKarp


def gen_random_string(dictionary, length):
    return ''.join(random.choices(dictionary, k=length))


def gen_string_from_string(str, length=None, **params):
    if length:
        return str[:length]
    else:
        return str


def generate_stat(algorithms,
                  set_params,
                  gen_string,
                  dictionary, reference_len, candidate_len,
                  n_observations,
                  **params):

    # sanity checks
    assert len(reference_len) == len(candidate_len)
    assert len(algorithms)    == len(set_params)
    for algorithm in algorithms:
        assert isinstance(algorithm(''), Algorithm)

    info_dct = {
                     'algorithm':     [],
                     'reference_len': [],
                     'candidate_len': [],
                     'preprocessing': [],
                     'execution':     [],
                     'observation':   [],
                     'indexes':       []
                   }

    for refer_len, candid_len in zip(reference_len, candidate_len):

        for observation in range(n_observations):

            reference = gen_string(dictionary, refer_len)
            candidate = gen_string(dictionary, candid_len)

            for algorithm, params in zip(algorithms, set_params):

                start_time = datetime.now()
                alg = algorithm(reference)
                alg.set_candidate(candidate, **params)
                preprocess = datetime.now() - start_time

                start_time = datetime.now()
                indexes = alg.search(multiple_search=True)
                execution = datetime.now() - start_time

                info_dct['algorithm']     += [alg.name]
                info_dct['reference_len'] += [refer_len]
                info_dct['candidate_len'] += [candid_len]
                info_dct['preprocessing'] += [preprocess.total_seconds()]
                info_dct['execution']     += [execution.total_seconds()]
                info_dct['observation']   += [observation]
                info_dct['indexes']       += [str(indexes)]

    return pd.DataFrame.from_dict(info_dct)


def get_plots(stat_df,
              figsize=(14, 6),
              title='Execution time of algorithms'):

    plt.figure(figsize=figsize)

    for alg in list(stat_df.algorithm.unique()):

        ox     = stat_df[stat_df.algorithm == alg]['reference_len']
        oy     = stat_df[stat_df.algorithm == alg]['execution mean']
        oy_std = stat_df[stat_df.algorithm == alg]['execution std']

        p = plt.plot(ox, oy, '.-', label=alg)
        plt.fill_between(ox,
                         oy - 3 * oy_std,
                         oy + 3 * oy_std,
                         color=p[0].get_color(), alpha=0.3,
                         label='Confidence interval of 95% ' + alg)
    plt.title(title)
    plt.xlabel('Reference string length')
    plt.ylabel('Time, seconds')
    plt.legend()
    plt.grid()
    plt.show()
