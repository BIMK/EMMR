import numpy as np
import pandas as pd
import heapq

dataset = 'ml-100k'
recommender = 'MF'
data = pd.read_csv('data/' + dataset + '.train', sep=',', header=None, usecols=[0, 1], names=["user", "item"])
# test = pd.read_csv('data/' + dataset + '.test', sep=',', header=None, usecols=[0, 1], names=["user", "item"])
all_rating = np.load('util_data/' + recommender + dataset + '_rating.npy', allow_pickle=True).item()
new_l = []
for key, value in all_rating.items():

    L = []
    rank = heapq.nlargest(100, value.items(), lambda x: x[1])
    buy_record = data.groupby('user')['item'].apply(list)
    a = set(list(value.keys())) & set(buy_record[key])
    num = len(a)
    new_l.append(num)
    b = set(list(value.keys())) ^ a
    for i in b:
        L.append(value[i])
    nnum = np.mean(new_l)
    pass
