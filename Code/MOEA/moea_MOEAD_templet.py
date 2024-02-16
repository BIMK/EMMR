# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # 导入geatpy库
from scipy.spatial.distance import cdist
from sys import path as paths
from os import path
import random
from tqdm import trange
from collections import Counter

paths.append(path.split(path.split(path.realpath(__file__))[0])[0])

def naiumber_of_certn_prob(seq, prob):
    x = random.uniform(0, 1)
    cumulative_prob = 0.0
    for item, item_prob in zip(seq, prob):
        cumulative_prob += item_prob
        if x < cumulative_prob:
            break
    return item

def indexA(listA,k):

    return [x for (x,m) in enumerate(listA) if m==k ]

# plist = []
# for i in range(100000):
#     plist.append(p_random([1, 2, 3], [0.209, 0.291, 0.5]))
# print(Counter(plist))
# # 输出结果：
# Counter({3: 50100, 2: 29132, 1: 20768})

def drop_duolicate(y1, y2, u, v,moea, user):
    b = dict(Counter(y1))
    for key, value in b.items():
        if value > 1:
            indexDict = indexA(y1, key)
            # index1 = set(indexDict).difference(range(u,v))
            # index2 = list(set(indexDict)&set(range(u,v)))
            # try:
            #     y1[list(index1)[0]] = y2[index2[0]]
            # except:
            for i in indexDict:
                try:
                    y1[i] = random.choice(list(set(y2).difference(y1)))
                    break
                except:
                    y1[i] = random.choice(list(set(moea.candidate[user].keys()).difference((list(y1)))))
                    break




    # indexDict = {}
    # listColunm = list(y1)
    # while listColunm.count(max(listColunm, key=listColunm.count)) > 1:  # 当元素个数 大于1时 进入循环
    #     intent = max(listColunm, key=listColunm.count)  # 找出重复元素
    #     position = listColunm.index(intent)  # 重复元素的第一个下标
    #     positionN = listColunm[position + 1:].index(intent) + (position + 1)  # 第N个重复元素的下标, 由于不是从0开始找 所以要把起始位置加上去
    #     # indexDict.append({intent: [position, positionN]})
    #     indexDict[intent] = [position, positionN]
    #     listColunm.pop(positionN)  # 删除重复元素, 不删除无法退出循环
    # for i in indexDict:
    #     index = set(indexDict[i]).differenct(range(u, v)))
    #     #     y1[list(index)[0]] = y2[list(set(indexDict[i])


    return y1




def naiumber_of_certn_prob(seq, prob):
    x = random.uniform(0, 1)
    cumulative_prob = 0.0
    for item, item_prob in zip(seq, prob):
        cumulative_prob += item_prob
        if x < cumulative_prob:
            break
    return item

def recombination(pop, moea, user):
    pop_list = list(range(pop.shape[0]))
    while len(pop_list) != 0:
        tmp1 = random.choice(pop_list)
        pop_list.remove(tmp1)
        tmp2 = random.choice(pop_list)
        pop_list.remove(tmp2)
        y1 = pop[tmp1].copy()
        y2 = pop[tmp2].copy()
        if np.random.rand() < 0.9:
            u = random.randrange(0, moea.n_rec_movie / 2)
            v = random.randrange(moea.n_rec_movie/2 + 1, moea.n_rec_movie) + 1
            # one-point crossover
            # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
            tmp = y1[u:v].copy()
            y1[u:v] = y2[u:v]
            y2[u:v] = tmp
            if len(set(y1)) != moea.n_rec_movie:
                y1 = drop_duolicate(y1,y2,u,v,moea, user)
            if len(set(y2)) != moea.n_rec_movie:
                y2 = drop_duolicate(y2,y1,u,v,moea, user)

        # pop[tmp1] = y1
        # pop[tmp2] = y2
        if np.random.rand() < 0.5:
            pop = y1
        else:
            pop = y2

    return pop


def recombination1(pop, pop2, moea):
    a = 0
    for chromosome in pop:
        a += 1
        for i in range(len(chromosome)):
            if np.random.rand() < moea.cross_rate:
                arr2 = []
                arr1 = list(set(pop2[:, i]))
                for x in arr1:
                    arr2.append(list((pop2[:, i])).count(x)/len(list((pop2[:, i]))))
                # chromosome[i] = p_random(arr1, arr2)
                chromosome[i] = naiumber_of_certn_prob(arr1, arr2)
        pop[a-1] = chromosome
    return pop


def recombination2(pop, moead):
    pop_list = list(range(pop.shape[0]))
    while len(pop_list) != 0:
        tmp1 = random.choice(pop_list)
        pop_list.remove(tmp1)
        tmp2 = random.choice(pop_list)
        pop_list.remove(tmp2)
        user_num = len(moead.user_index)
        y1 = pop[tmp1].copy()
        y2 = pop[tmp2].copy()
        for i in range(user_num):
            # crossover_rate
            if np.random.rand() < moead.cross_rate:
                u = random.randrange(0, moead.recommendation_len / 2)
                v = random.randrange(moead.recommendation_len/2 + 1, moead.recommendation_len) + 1
                # one-point crossover
                # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
                tmp = y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v].copy()
                y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v]
                y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = tmp

                # u = random.randrange(0, moead.recommendation_len)
                # # one-point crossover
                # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
        # pop[tmp1] = y1
        # pop[tmp2] = y2

    return pop



# def recombination(pop_all, moead):
#     user_num = len(moead.user_index)
#     pop = pop_all.Chrom
#     pop_list = list(range(pop.shape[0]))
#     while len(pop_list) != 0:
#         tmp1 = random.choice(pop_list)
#         pop_list.remove(tmp1)
#         tmp2 = random.choice(pop_list)
#         pop_list.remove(tmp2)
#         result = pop_all.ObjV[tmp1] < pop_all.ObjV[tmp2]
#         if result[0] == True and result[1] == True:
#         # if result[0] == True and result[1] == True and result[2] == True:
#
#             win = tmp1
#             loss = tmp2
#             for i in range(len(pop[win])):
#                     if np.random.rand() < moead.cross_rate:
#                         pop[loss][i] = pop[win][i]
#         # elif result[0] == False and result[1] == False and result[2] == False:
#         elif result[0] == False and result[1] == False:
#             win = tmp2
#             loss = tmp1
#             for i in range(len(pop[win])):
#                     if np.random.rand() < moead.cross_rate:
#                         pop[loss][i] = pop[win][i]
#         else:
#             y1 = pop[tmp1].copy()
#             y2 = pop[tmp2].copy()
#             for i in range(user_num):
#                     # crossover_rate
#                     if np.random.rand() < moead.cross_rate:
#                         u = random.randrange(0, moead.recommendation_len/2)
#                         v = random.randrange(moead.recommendation_len/2 + 1, moead.recommendation_len)
#                         # one-point crossover
#                         # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
#                         y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v], y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v], y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v]
#
#             pop[tmp2] = y2
#             pop[tmp1] = y1
#
#     return pop

def mutation(pop, moea, user):


    if np.random.rand() < 0.2:
        u = random.randrange(0, moea.n_rec_movie)
        candidate = list(set(moea.candidate).difference((list(pop)))) # choose a different item
        if len(candidate) > 0:
            pop[u] = random.choice(candidate)

    return pop

class moea_MOEAD_templet(ea.MoeaAlgorithm):
    """
moea_MOEAD_templet : class - 多目标进化MOEA/D算法模板（采用可行性法则处理约束）
    
算法描述:
    采用MOEA/D（不设全局最优存档）进行多目标优化，算法详见参考文献[1]。
    注：MOEA/D不适合在Python上实现，在Python上，MOEA/D的性能会大幅度降低。

参考文献:
    [1] Qingfu Zhang, Hui Li. MOEA/D: A Multiobjective Evolutionary Algorithm 
    Based on Decomposition[M]. IEEE Press, 2007.

    """

    def __init__(self, problem, population):
        ea.MoeaAlgorithm.__init__(self, problem, population)  # 先调用父类构造方法
        if population.ChromNum != 1:
            raise RuntimeError('传入的种群对象必须是单染色体的种群类型。')
        self.name = 'MOEA/D'
        if population.Encoding == 'P':
            self.recOper = ea.Xovpmx(XOVR=1, Half_N=True)  # 生成部分匹配交叉算子对象
            self.mutOper = ea.Mutinv(Pm=1)  # 生成逆转变异算子对象
        elif population.Encoding == 'BG':
            self.recOper = ea.Xovud(XOVR=1, Half_N=True)  # 生成均匀交叉算子对象
            self.mutOper = ea.Mutbin(Pm=None)  # 生成二进制变异算子对象，Pm设置为None时，具体数值取变异算子中Pm的默认值
        elif population.Encoding == 'RI':
            # self.recOper = ea.Recsbx(XOVR=1, n=20, Half_N=True)  # 生成模拟二进制交叉算子对象
            self.recOper = ea.Xovud(XOVR=1, Half_N=True)  # 生成均匀交叉算子对象
            self.mutOper = ea.Mutpolyn(Pm=1 / self.problem.Dim, DisI=20)  # 生成多项式变异算子对象
        # else:
        #     raise RuntimeError('编码方式必须为''BG''、''RI''或''P''.')
        self.neighborSize = 5  # 邻域大小，当设置为None时，将会自动设置为等于种群规模
        if self.problem.M <= 2:
            self.decomposition = ea.tcheby  # 采用切比雪夫权重聚合法
        else:
            self.decomposition = ea.pbi  # 采用pbi权重聚合法
        self.Ps = 0.9  # (Probability of Selection)表示进化时有多大的概率只从邻域中选择个体参与进化

    def reinsertion(self, indices, population, offspring, idealPoint, referPoint):

        """
        描述:
            重插入更新种群个体。
        """

        weights = referPoint[indices, :]
        pop_ObjV = population.ObjV[indices, :]  # 获取邻居个体的目标函数值
        pop_CV = population.CV[indices, :] if population.CV is not None else None  # 获取邻居个体的违反约束程度矩阵
        CombinObjV = self.decomposition(pop_ObjV, weights, idealPoint, pop_CV, self.problem.maxormins)
        off_CombinObjV = self.decomposition(offspring.ObjV, weights, idealPoint, offspring.CV, self.problem.maxormins)
        population[indices[np.where(off_CombinObjV <= CombinObjV)[0]]] = offspring

    def run(self, prophetPop=None, moea=None):  # prophetPop为先知种群（即包含先验知识的种群）
        # ==========================初始化配置===========================
        population = self.population
        self.initialization()  # 初始化算法模板的一些动态参数
        # ===========================准备进化============================
        uniformPoint, NIND = ea.crtup(self.problem.M, population.sizes)  # 生成在单位目标维度上均匀分布的参考点集
        population.initChrom(self.user,NIND,moea=moea)  # 初始化种群染色体矩阵，此时种群规模将调整为uniformPoint点集的大小，initChrom函数会把种群规模给重置
        self.call_aimFunc(population)  # 计算种群的目标函数值
        # 插入先验知识（注意：这里不会对先知种群prophetPop的合法性进行检查，故应确保prophetPop是一个种群类且拥有合法的Chrom、ObjV、Phen等属性）
        if prophetPop is not None:
            population = (prophetPop + population)[:NIND]  # 插入先知种群
        # 确定邻域大小
        if self.neighborSize is None:
            self.neighborSize = population.sizes
        self.neighborSize = max(self.neighborSize, 2)  # 确保不小于2
        # 生成由所有邻居索引组成的矩阵
        neighborIdx = np.argsort(cdist(uniformPoint, uniformPoint), axis=1, kind='mergesort')[:, :self.neighborSize]
        # 计算理想点
        idealPoint = ea.crtidp(population.ObjV, population.CV, self.problem.maxormins)
        # ===========================开始进化============================
        while self.terminated(population) == False:
            select_rands = np.random.rand(population.sizes)  # 生成一组随机数
            for i in range(population.sizes):
                indices = neighborIdx[i, :]  # 得到邻居索引
                if select_rands[i] < self.Ps:
                    chooseIdx = indices[ea.rps(self.neighborSize, 2)]  # 只从邻域中选择
                else:
                    chooseIdx = ea.rps(population.sizes, 2)
                matting_Chrom = population.Chrom[chooseIdx, :]  # 选出2条来自被选个体的染色体
                offspring = ea.Population(population.Encoding, population.Field, 1)  # 实例化一个种群对象用于存储进化的后代（这里只进化生成一个后代）
                # 对选出的个体进行进化操作
                # offspring.Chrom = recombination2(matting_Chrom, moea)
                offspring.Chrom = recombination(matting_Chrom,moea,self.user)  # 重组
                offspring.Chrom = mutation(offspring.Chrom, moea, self.user)
                # offspring.Chrom = self.mutOper.do(offspring.Encoding, offspring.Chrom, offspring.Field)  # 变异
                self.call_aimFunc(offspring)  # 求进化后个体的目标函数值
                # 更新理想点
                idealPoint = ea.crtidp(offspring.ObjV, offspring.CV, self.problem.maxormins, idealPoint)
                # 重插入更新种群个体
                self.reinsertion(indices, population, offspring, idealPoint, uniformPoint)
        return self.finishing(population)  # 调用finishing完成后续工作并返回结果
