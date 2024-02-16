# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # 导入geatpy库
from sys import path as paths
from os import path
import random
from tqdm import trange
from collections import Counter


paths.append(path.split(path.split(path.realpath(__file__))[0])[0])

def indexA(listA,k):

    return [x for (x,m) in enumerate(listA) if m==k ]

# def p_random(arr1, arr2):
#     assert len(arr1) == len(arr2), "Length does not match."
#     # assert sum(arr2) == 1, "Total rate is not 1."
#
#     sup_list = [len(str(i).split(".")[-1]) for i in arr2]
#     top = 10 ** max(sup_list)
#     new_rate = [int(i * top) for i in arr2]
#     rate_arr = []
#     for i in range(1, len(new_rate) + 1):
#         rate_arr.append(sum(new_rate[:i]))
#     rand = random.randint(1, top)
#     data = None
#     for i in range(len(rate_arr)):
#         if rand <= rate_arr[i]:
#             data = arr1[i]
#             break
#     return data

def drop_duolicate(y1, y2, moea):
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
                    y1[i] = random.choice(list(set(moea.candidate.keys()).difference((list(y1)))))
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

def recombination(pop, moea):
    pop_list = list(range(pop.shape[0]))
    while len(pop_list) != 0:
        tmp1 = random.choice(pop_list)
        pop_list.remove(tmp1)
        tmp2 = random.choice(pop_list)
        pop_list.remove(tmp2)
        y1 = pop[tmp1].copy()
        y2 = pop[tmp2].copy()
        if np.random.rand() < 0.9:
            # u = random.randrange(0, moea.n_rec_movie / 2)
            # v = random.randrange(moea.n_rec_movie/2 + 1, moea.n_rec_movie) + 1
            u = random.randint(0, 1)
            v = random.randint(3, 4)
            # one-point crossover
            # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
            tmp = y1[u:v].copy()
            y1[u:v] = y2[u:v]
            y2[u:v] = tmp
            if len(set(y1)) != moea.n_rec_movie:
                y1 = drop_duolicate(y1,y2,moea)
            if len(set(y2)) != moea.n_rec_movie:
                y2 = drop_duolicate(y2,y1,moea)

        pop[tmp1] = y1
        pop[tmp2] = y2

    return pop



# plist = []
# for i in range(100000):
#     plist.append(p_random([1, 2, 3], [0.209, 0.291, 0.5]))
# print(Counter(plist))
# # 输出结果：
# Counter({3: 50100, 2: 29132, 1: 20768})

# def recombination1(pop, pop2, moea):
#     a = 0
#     for chromosome in pop:
#         a += 1
#         for i in range(len(chromosome)):
#             if np.random.rand() < moea.cross_rate:
#                 arr2 = []
#                 arr1 = list(set(pop2[:, i]))
#                 for x in arr1:
#                     arr2.append(list((pop2[:, i])).count(x)/len(list((pop2[:, i]))))
#                 # chromosome[i] = p_random(arr1, arr2)
#                 chromosome[i] = naiumber_of_certn_prob(arr1, arr2)
#         pop[a-1] = chromosome
#     return pop
#
#
# def recombination2(pop, moead):
#     pop_list = list(range(pop.shape[0]))
#     while len(pop_list) != 0:
#         tmp1 = random.choice(pop_list)
#         pop_list.remove(tmp1)
#         tmp2 = random.choice(pop_list)
#         pop_list.remove(tmp2)
#         user_num = len(moead.user_index)
#         y1 = pop[tmp1].copy()
#         y2 = pop[tmp2].copy()
#         for i in range(user_num):
#             # crossover_rate
#             if np.random.rand() < moead.cross_rate:
#                 u = random.randrange(0, moead.recommendation_len / 2)
#                 v = random.randrange(moead.recommendation_len/2 + 1, moead.recommendation_len) + 1
#                 # one-point crossover
#                 # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
#                 tmp = y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v].copy()
#                 y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v]
#                 y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = tmp
#                 # u = random.randrange(0, moead.recommendation_len)
#                 # # one-point crossover
#                 # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
#         pop[tmp1] = y1
#         pop[tmp2] = y2
#
#     return pop
#
#
#
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
#                         rn = random.sample(range(10), random.randint(0, 9))
#                         rn = list(map(lambda x: x+(i * moead.recommendation_len), rn))
#                         tmp = y1[rn]
#                         y1[rn] = y2[rn]
#                         y2[rn] = tmp
#                         # u = random.randrange(0, moead.recommendation_len/2)
#                         # v = random.randrange(moead.recommendation_len/2 + 1, moead.recommendation_len)
#                         # # one-point crossover
#                         # # y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len] = y2[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len], y1[i * moead.recommendation_len + u:(i + 1) * moead.recommendation_len]
#                         # tmp = y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v].copy()
#                         # y1[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v]
#                         # y2[i * moead.recommendation_len + u:i * moead.recommendation_len + v] = tmp
#             pop[tmp2] = y2
#             pop[tmp1] = y1
#
#     return pop

def mutation(pop, moea):
    a = 0
    for chromosome in pop:
        a += 1
        if np.random.rand() < 0.2:
            u = random.randrange(0, moea.n_rec_movie)
            candidate = list(set(moea.candidate).difference((list(chromosome)))) # choose a different item
            if len(candidate) > 0:
                chromosome[u] = random.choice(candidate)
        pop[a - 1] = chromosome
        return pop


class moea_NSGA2_templet(ea.MoeaAlgorithm):
    """
moea_NSGA2_templet : class - 多目标进化NSGA-II算法模板
    
算法描述:
    采用NSGA-II进行多目标优化，算法详见参考文献[1]。

参考文献:
    [1] Deb K , Pratap A , Agarwal S , et al. A fast and elitist multiobjective 
    genetic algorithm: NSGA-II[J]. IEEE Transactions on Evolutionary 
    Computation, 2002, 6(2):0-197.

    """

    def __init__(self, problem, population):
        ea.MoeaAlgorithm.__init__(self, problem, population)  # 先调用父类构造方法
        if population.ChromNum != 1:
            raise RuntimeError('传入的种群对象必须是单染色体的种群类型。')
        self.name = 'NSGA2'
        if self.problem.M < 10:
            self.ndSort = ea.ndsortESS  # 采用ENS_SS进行非支配排序
        else:
            self.ndSort = ea.ndsortTNS  # 高维目标采用T_ENS进行非支配排序，速度一般会比ENS_SS要快
        self.selFunc = 'tour'  # 选择方式，采用锦标赛选择
        # if population.Encoding == 'P':
        #     self.recOper = ea.Xovpmx(XOVR=1)  # 生成部分匹配交叉算子对象
        #     self.mutOper = ea.Mutinv(Pm=1)  # 生成逆转变异算子对象
        # elif population.Encoding == 'BG':
        #     self.recOper = ea.Xovud(XOVR=1)  # 生成均匀交叉算子对象
        #     self.mutOper = ea.Mutbin(Pm=None)  # 生成二进制变异算子对象，Pm设置为None时，具体数值取变异算子中Pm的默认值
        # elif population.Encoding == 'RI':
        #     self.recOper = ea.Recsbx(XOVR=1, n=20)  # 生成模拟二进制交叉算子对象
        #     self.mutOper = ea.Mutpolyn(Pm=1 / self.problem.Dim, DisI=20)  # 生成多项式变异算子对象
        # else:
        #     raise RuntimeError('编码方式必须为''BG''、''RI''或''P''.')

    def reinsertion(self, population, offspring, NUM):

        """
        描述:
            重插入个体产生新一代种群（采用父子合并选择的策略）。
            NUM为所需要保留到下一代的个体数目。
            注：这里对原版NSGA-II进行等价的修改：先按帕累托分级和拥挤距离来计算出种群个体的适应度，
            然后调用dup选择算子(详见help(ea.dup))来根据适应度从大到小的顺序选择出个体保留到下一代。
            这跟原版NSGA-II的选择方法所得的结果是完全一样的。
        """

        # 父子两代合并
        population = population + offspring
        # 选择个体保留到下一代
        [levels, criLevel] = self.ndSort(population.ObjV, NUM, None, population.CV,
                                         self.problem.maxormins)  # 对NUM个个体进行非支配分层
        dis = ea.crowdis(population.ObjV, levels)  # 计算拥挤距离
        population.FitnV[:, 0] = np.argsort(np.lexsort(np.array([dis, -levels])), kind='mergesort')  # 计算适应度
        chooseFlag = ea.selecting('dup', population.FitnV, NUM)  # 调用低级选择算子dup进行基于适应度排序的选择，保留NUM个个体
        return population[chooseFlag]



    # def run(self, prophetPop=None, moea=None):  # prophetPop为先知种群（即包含先验知识的种群）
    #     # ==========================初始化配置===========================
    #     population = self.population
    #     NIND = population.sizes
    #     self.initialization()  # 初始化算法模板的一些动态参数
    #     # ===========================准备进化============================
    #     population.initChrom(moea=moea)  # 初始化种群染色体矩阵
    #     self.call_aimFunc(population)  # 计算种群的目标函数值
    #     # 插入先验知识（注意：这里不会对先知种群prophetPop的合法性进行检查，故应确保prophetPop是一个种群类且拥有合法的Chrom、ObjV、Phen等属性）
    #     if prophetPop is not None:
    #         population = (prophetPop + population)[:NIND]  # 插入先知种群
    #     [levels, criLevel] = self.ndSort(population.ObjV, NIND, None, population.CV,
    #                                      self.problem.maxormins)  # 对NIND个个体进行非支配分层
    #     population.FitnV = (1 / levels).reshape(-1, 1)  # 直接根据levels来计算初代个体的适应度
    #     # ===========================开始进化============================
    #    # while self.terminated(population) == False:
    #     for _ in trange(self.MAXGEN):
    #         # 选择个体参与进化
    #         [levels, criLevel] = self.ndSort(population.ObjV, NIND, None, population.CV,
    #                                          self.problem.maxormins)  # 对NIND个个体进行非支配分层
    #         if len(np.where(levels == 1)[0]) != NIND:
    #             NDset = population[np.where(levels == 1)[0]]
    #             offspring2 = population[np.where(levels != 1)[0]]
    #             offspring2.Chrom = recombination1(offspring2.Chrom, NDset.Chrom, moea)
    #             offspring = offspring2 + NDset
    #             offspring.Chrom = mutation(offspring.Chrom, moea)  # 变异
    #         else:
    #             offspring = population[ea.selecting(self.selFunc, population.FitnV, NIND)]
    #             offspring.Chrom = recombination2(offspring.Chrom, moea)
    #             offspring.Chrom = mutation(offspring.Chrom, moea)
    #         self.call_aimFunc(offspring)  # 求进化后个体的目标函数值
    #         population = self.reinsertion(population, offspring, NIND)  # 重插入生成新一代种群
    #     return self.finishing(population)  # 调用finishing完成后续工作并返回结果

    def run(self, prophetPop=None, moea=None):  # prophetPop为先知种群（即包含先验知识的种群）
        # ==========================初始化配置===========================
        population = self.population
        NIND = population.sizes
        self.initialization()  # 初始化算法模板的一些动态参数
        # ===========================准备进化============================
        population.initChrom(moea=moea)  # 初始化种群染色体矩阵
        self.call_aimFunc(population)  # 计算种群的目标函数值
        # 插入先验知识（注意：这里不会对先知种群prophetPop的合法性进行检查，故应确保prophetPop是一个种群类且拥有合法的Chrom、ObjV、Phen等属性）
        if prophetPop is not None:
            population = (prophetPop + population)[:NIND]  # 插入先知种群
        [levels, criLevel] = self.ndSort(population.ObjV, NIND, None, population.CV,
                                         self.problem.maxormins)  # 对NIND个个体进行非支配分层
        population.FitnV = (1 / levels).reshape(-1, 1)  # 直接根据levels来计算初代个体的适应度
        obj1 = []
        obj2 = []
        # ===========================开始进化============================
        while self.terminated(population) == False:
        # for _ in trange(self.MAXGEN):
            # 选择个体参与进化
            # offspring = population[ea.selecting(self.selFunc, population.FitnV, NIND)]
            offspring = population
            # 对选出的个体进行进化操作
            offspring.Chrom = recombination(offspring.Chrom, moea)  # 重组
            offspring.Chrom = mutation(offspring.Chrom,moea)  # 变异
            self.call_aimFunc(offspring)  # 求进化后个体的目标函数值
            population = self.reinsertion(population, offspring, NIND)  # 重插入生成新一代种群
            # if self.evalsNum % 10 == 0:
            obj1.append(np.mean(population.ObjV[:, 0]))
            obj2.append(np.mean(population.ObjV[:, 1]))

        return self.finishing(population), population.ObjV, obj1, obj2# 调用finishing完成后续工作并返回结果


