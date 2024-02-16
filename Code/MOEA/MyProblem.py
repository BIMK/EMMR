# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""
该案例展示了一个带约束连续决策变量的最小化目标的双目标优化问题。
min f1 = X**2
min f2 = (X - 2)**2
s.t.
X**2 - 2.5 * X + 1.5 >= 0
10 <= Xi <= 10, (i = 1,2,3,...)
"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, score):
        self.moea = score
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        Dim = self.moea.n_rec_movie  # 初始化Dim（决策变量维数）
        if self.moea.model == 1 or self.moea.model == 2:
            M = 2
            maxormins = [-1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        elif self.moea.model == 3:
            M = 3
            maxormins = [-1] * M
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        ub = [self.moea.movie_count] * Dim  # 决策变量上界
        lbin = [0] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        X = pop.Phen  # 得到决策变量矩阵
        f1 = Precision(X, self.moea.rating_matrix)
        f2 = Novelty(X, self.moea.Mi)
        f3 = Diversity(X, self.moea.Si, self.moea.div_max, self.moea.si_spilt)
        if self.moea.model == 1:
            pop.ObjV = np.vstack([f1, 1-f2]).T # 把求得的目标函数值赋值给种群pop的ObjV
        elif self.moea.model == 2:
            pop.ObjV = np.vstack([f1, f3]).T
        elif self.moea.model == 3:
            pop.ObjV = np.vstack([f1, 1-f2, f3]).T
        # pop.ObjV = np.vstack([1 - f1, f2, 1 - f3]).T # 把求得的目标函数值赋值给种群pop的ObjV

def Precision(X, rank):
    fin_pre = []
    for a in X:
        ave_pre = 0.0
        for i in a:
            ave_pre += rank[i]
        fin_pre.append(ave_pre/len(a))
    return np.array(fin_pre)

def Novelty(X, item_interact_frequency):
    fin_nov = []
    for a in X:
        novelty = 0.0
        for i in a:
            novelty += item_interact_frequency[i]
        fin_nov.append((novelty/len(a))/item_interact_frequency.max())
    return np.array(fin_nov)

def Diversity(X, div_list, max, st):
    fin_div = []
    for a in X:
        div = ""
        for item in a:
            try:
                div = div + st + div_list['genre'][item]
            except:
                pass
        result = np.unique(div.split(st))
        fin_div.append((len(result) - 1)/max)
    return np.array(fin_div)

