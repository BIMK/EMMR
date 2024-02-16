import time
import numpy as np
import pandas as pd
from tqdm import trange


from utils import Dataset
from evaluate_pop import evaluate_all
from MOEA.moea import MOEA

def minmax(List):
    return (np.mean(List)-min(List))/(max(List)-min(List))


class scoer():
    def __init__(self, rating, Mi, buy_record, maxdiv, st, Si):
        self.n_rec_movie = 10
        self.movie_count = len(Mi)
        self.candidate = list(rating.keys())
        self.buy_record = buy_record
        self.Si = Si
        self.Mi = Mi
        self.rating_matrix = rating
        self.model = 1
        #model=1 pre+nov; model=2 pre+div;model=3 pre+nov+div
        self.div_max = maxdiv
        self.si_spilt = st

if __name__ == "__main__":
    # rec_user = [301, 339, 824, 182, 283, 633]
    # rec_list = np.empty([len(rec_user), 10])
    # tmp = -1
    t1 = time.time()
    dataset = 'anime'
    recommender = 'LightGCN'
    if dataset == 'anime':
        maxdiv = 82
        st = ','
    elif dataset == 'ml-10m':
        maxdiv = 20
        st = '|'
    elif dataset == 'Music':
        maxdiv = 404
        st = ','
    Data = Dataset('data/' + dataset +'.train')
    Si = pd.read_csv('util_data/' + dataset + '_div.csv', sep=',', header=None, usecols=[0, 1], names=["item", "genre"])
    test = pd.read_csv('data/' + dataset +'.test', sep=',', usecols=[0, 1], names=["user", "item"])
    real_lable = test.groupby('user')['item'].apply(list)
    rating = np.load('util_data/' + recommender + dataset + '_rating.npy', allow_pickle=True).item()
    user_num = Data.user_num
    Pre, Novelt, Hit, Diversity = [], [], [], []
    Obj = ([], [])
    for u in trange(user_num):
    # for u in trange(5):
        # tmp+=1
        try:
            real_lable[u]
        except:
            continue
        Scoer = scoer(rating[u], Data.Mi, Data.buy_record[u], maxdiv, st, Si)
        moea = MOEA(Scoer)
        [populationt, NDSet], ObjV, obj1, obj2 = moea.myAlgorithm.run(moea=Scoer)
    #     rec_list[tmp] = NDSet.Chrom[0]
    #
    # np.save(recommender + dataset + "_reclist", rec_list)

        Obj[0].append(obj1)
        Obj[1].append(obj2)

        # Obj[0].append(ObjV[:,0])
        # Obj[1].append(ObjV[:,1])
        recall, novelty, diversity, hit = evaluate_all(NDSet.Chrom, Scoer, real_lable[u])
        Pre.append(recall)
        Diversity.append(diversity)
        Novelt.append(novelty)
        Hit.append(hit)
        if u == 50:
            np.save(recommender + dataset + "_objective_trac_old", Obj)
            break
    print('precisioin=%.4f\tdiversity=%.4f\tnovelty=%.4f\thit=%.4f\ttime=%.4f\t' % (
    np.mean(Pre), np.mean(Diversity), np.mean(Novelt), np.mean(Hit),
    time.time() - t1))
    print(dataset, recommender, moea.myAlgorithm.MAXGEN, moea.myAlgorithm.population.sizes, max(Novelt))


