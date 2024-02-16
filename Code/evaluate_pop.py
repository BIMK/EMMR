import random

import numpy as np

def Trade_off(F1, F2):
    F1_score = (2*F1*F2)/(F1+F2)
    k = np.where(F1_score == np.max(F1_score))[0]
    return k[0]



def evaluate_all(NDSet, moead, test):
    Hit ,Recall, Novelty, Diversity = [], [], [], []
    for k in range(len(NDSet)):
        recall, hit = evaluate_result_Precision_individual_k(test, NDSet[k])
        diversity = evaluate_result_DIVERSITY_k(moead, NDSet[k])
        novelty = evaluate_result_Novelty_individual_k(moead.Mi, NDSet[k])
        Recall.append(recall)
        Novelty.append(novelty)
        Diversity.append(diversity)
        Hit.append(hit)
    if moead.model == 1:
        K = Trade_off(np.array(Recall), np.array(Novelty))
    elif moead.model == 2:
        K = Trade_off(np.array(Recall), np.array(Diversity))
    elif moead.model == 3:
        K = random.choice(range(len(NDSet)))

    return Recall[K], Novelty[K], Diversity[K], Hit[K]

def evaluate_result_Precision_individual_k(real_label, X):
    recall = len(set(X) & set(real_label)) / len(real_label)
    hit = len(set(X) & set(real_label)) / len(set(X))
    return recall, hit

def evaluate_result_Novelty_individual_k(Mi, X):  # k-th individual in population
    Novelty = 0.0
    for i in X:
        Novelty += Mi[i]
    return 1 - ((Novelty / len(X))/Mi.max())

def evaluate_result_DIVERSITY_k(moead, X):
    div = ""
    for item in X:
        try:
            div = div + moead.si_spilt + moead.Si['genre'][item]
        except:
            pass
    result = np.unique(div.split(moead.si_spilt))
    return (len(result) - 1)/moead.div_max