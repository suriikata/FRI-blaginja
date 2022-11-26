import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from Orange.data import Table
from Orange.preprocess.score import UnivariateLinearRegression, RReliefF
from Orange.regression.random_forest import RandomForestRegressionLearner

from feature_subset_selection import get_top_attributes, rf_top_attributes

data = Table("C:\\Users\irisc\Documents\FRI\\blaginja\FRI-blaginja\SEI_krajsi_A008.W_selected.pkl")


def get_forest_scores(data):
    rank_scores = []
    for x in range(100):
        np.random.shuffle(data.Y)
        method = RandomForestRegressionLearner(n_estimators=100, min_samples_split=5, random_state=0)
        scores = method.score(data)[0]
        for score in scores:
            rank_scores.append(score)
    rank_scores_clean = [x for x in rank_scores if not np.isnan(x)]  # x != 0.0

    print(len(rank_scores_clean))
    return rank_scores_clean


def get_ranker_scores(ranker, data):
    rank_scores = []
    for x in range(100):
        np.random.shuffle(data.Y)
        scores = ranker(data)
        for score in scores:
            rank_scores.append(score)
    rank_scores_clean = [x for x in rank_scores if not np.isnan(x)]         # x != 0.0

    print(len(rank_scores_clean))
    return rank_scores_clean

def plot_dist(scores):
    plt.figure(figsize=(14,16))
    sns.histplot(data=scores).set(title="regresijski srečkovič")
    plt.show()


def calculate_p_value(distribution, top_score):
    """
    cnt = count the number of values in the distribution that are bigger than sample
    p_val = cnt / len(distribution)
    """
    cnt = 0
    for score in distribution:
        if score >= top_score:
            cnt += 1
    p_val = cnt / len(distribution)
    return p_val


def get_ranker_p_values(random_scores, top_factors):
    p_values = {}
    for score, att_name in top_factors:
        p_val = calculate_p_value(random_scores, score)
        #scores_p_val.append(p_val)
        p_values[att_name] = p_val
    print(p_values)
    return p_values


def get_p_values_for_top_factors(data):
    relief_top_factors = get_top_attributes(RReliefF(random_state=0), data)
    linear_top_factors = get_top_attributes(UnivariateLinearRegression(), data)
    random_top_factors = rf_top_attributes(data)

    seznam = [relief_top_factors, linear_top_factors, random_top_factors]

    ranker_scores = []
    for ranker in [RReliefF(random_state=0), UnivariateLinearRegression()]:
        ranker_scores.append(get_ranker_scores(ranker, data))
    ranker_scores.append(get_forest_scores(data))


    slovarcki = []
    for random_scores, top_factors in zip(ranker_scores, seznam):
        p_values = get_ranker_p_values(random_scores, top_factors)
        print(p_values)
        slovarcki.append(p_values)
    return slovarcki


def google(ime_datoteke):
    google = True
    if google:
        with open(f'{ime_datoteke}.csv') as f:
            tabela_str = f.read()
        tabela_str = tabela_str.replace(',', ':').replace('.', ',')
        with open(f'{ime_datoteke}.txt', 'w') as f:
            f.write(tabela_str)
        print(f"za google zapisano v {ime_datoteke}.txt")


get_p_values_for_top_factors(data)


"""
rez = get_p_value(ranker_scores)
plot_dist(ranker_scores)
"""