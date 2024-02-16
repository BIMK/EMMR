import geatpy as ea  # import geatpy
from MOEA.MyProblem import MyProblem  # 导入自定义问题接口
from MOEA.Population import Population
from MOEA.moea_NSGA2_templet import moea_NSGA2_templet
# from MOEA.moea_MOEAD_templet import moea_MOEAD_templet
class MOEA:
    def __init__(self, score):
        problem = MyProblem(score)
        Encoding = 'RI'  # 编码方式
        NIND = 10  # 种群规模.
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders,
                          [10] * len(problem.varTypes))  # 创建区域描述器
        population = Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        myAlgorithm = moea_NSGA2_templet(problem, population)
        myAlgorithm.neighborSize = 100
        myAlgorithm.MAXGEN = 100 # 最大进化代数
        myAlgorithm.logTras = 0  # 设置每多少代记录日志，若设置成0则表示不记录日志
        myAlgorithm.verbose = False  # 设置是否打印输出日志信息
        myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画
        self.myAlgorithm = myAlgorithm
        # print("finish initial\n")

