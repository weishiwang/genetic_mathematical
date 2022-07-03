import random
import pandas as pd
import copy


sumzhongqun = 200
jiaochagailv = 0.5 #交叉概率
bianyigailv = 0.3#变异概率
childmostfitness=[]#记录每一个子代的最优表达式
most_fit=''#记录目前为止最优的表达式
most_bdss=[]#记录每最优个体的变化
look_most_bdss=[]
most_bds_value =[]#最优表达式的的y值
most_fitness_change = []#记录适应度的变化过程
diedaishu=1000
danxishu_long=13#基因单系数长
#----------------------------中缀表达式求值------------------------------------
class Stack():#定义一个栈
    def __init__(self,):
        self.stack = []
    def push(self,data):#入栈
        self.stack.append(data)
    def pop(self):#出栈
        return self.stack.pop()
    def is_empty(self):#是否栈空
        return not len(self.stack)
    def top(self):#栈顶元素
        if self.is_empty():
            return None
        return self.stack[-1]




class InversPolishCalculator(object):#逆波兰计算器

    def deal(self,exspression):#主程序,传入中缀表达式,返回结果
        list_expression = self.get_list_expression(exspression)
        stack = Stack() # 实例化栈
        for ele in list_expression: # 处理逆波兰表达式
            if ele.replace('.','').isdigit(): # 是数字压入栈
                stack.push(ele)
            else: # 是运算符进行运算,用次顶元素,和栈顶元素
                ret = self.operation(ele, float(stack.pop()), float(stack.pop()))
                stack.push(ret)
        return '%.2f'% stack.pop()#返回结果

    def operation(self,sign, num2, num1): # 定义算法
        if sign == '*':
            return num1 * num2
        if sign == '/':

            return num1/num2
        if sign == '+':
            return num1 + num2
        if sign == '-':
            return num1 - num2

    def deal_str(self,exspression):#处理中缀表达式字符串,转为列表形式方便计算
        status = 0
        res = ''
        exspression = exspression.strip().replace(' ','')
        for ele in exspression:
            if ele.isdigit() or ele =='.':
                if status == 1:
                    res =res.strip(' ')
                    res = res + ele + ' '
                else:
                    status = 1
                    res= res+ele+' '
            else:
                status = 0
                res = res + ele + ' '
        return res.strip().split(' ')

    def get_list_expression(self,exspression):#将中缀表达式列表形式转后缀
        lst = self.deal_str(exspression)
        s1 = Stack()
        s2 = Stack()
        for ele in lst:
            if ele.replace('.','').isdigit():
                s2.push(ele)
            else:
                self.deal_symbol(ele,s1,s2)
        while not s1.is_empty():
            s2.push(s1.pop())
        res = []
        while not s2.is_empty():
            res.append(s2.pop())
        return res[::-1]

    def deal_symbol(self,ele,s1,s2):#处理符号入栈出栈问题
        if s1.is_empty() or s1.top() == '(' or ele == '(':
            s1.push(ele)
        elif ele == ')':
            while s1.top() != '(':
                s2.push(s1.pop())
            s1.pop()
        elif self.get_priority(ele) > self.get_priority(s1.top()):
            s1.push(ele)
        else:
            s2.push(s1.pop())
            self.deal_symbol(ele,s1,s2)

    def get_priority(self,sign):#获取符号优先级
        if sign=='*' or sign=='/':
            return 2
        elif sign=='+' or sign=='-':
            return 1
#----------------------------中缀表达式求值------------------------------------
           
       
#------------------读入数据并生成第一代表达式-----------------------------------

data = pd.read_excel('data.xls')
col = data.columns.to_list()#除了最后一项外其他全部是自变量

for i in range(len(col)-1):
    data[col[i]]=data[col[i]].apply(str)

suanshu=['+','-','*','/']
xishu=['1','2','3','4','5','6','7','8','9']
first=[]
for i in range(sumzhongqun):#后面要改成种群个数
    biaodashi=''
    for j in range(len(col)-1):#减去一个因变量
        a=random.randint(0,1)#次数
        b=random.randint(0,3)#算术
        c=random.randint(1,50)#系数
        c_2=format(int(c),'08b')
        if(a==0):
            biaodashi=biaodashi+c_2+'***1'
        elif(a==1):
            biaodashi=biaodashi+c_2+'***2'
        biaodashi=biaodashi+suanshu[b]
    biaodashi=biaodashi[0:-1]
    first.append(biaodashi)

#------------------读入数据并生成第一代表达式-----------------------------------

#----生成每一个表达式的种群并且计算每一个种群中每一个个体的数学表达式的值---------
   
def dairubiaodashi(first):
    bds=[[]for i in range(sumzhongqun)]
    for i in range(sumzhongqun):
        bianlianggeshu=len(col)-1
       
        for j in range(len(data.x1)):
            shi=''
#            代码优化
            for k in range(bianlianggeshu-1):#a***2+b***2+c***2每六个算是一个系数最后一组除外

                if(first[i][9+danxishu_long*k:12+danxishu_long*k]=='**2'):#a***2+a***2+a***2每六个算是一个系数最后一组除外
                    shi=shi+str(int(first[i][0+danxishu_long*k:8+danxishu_long*k], 2))+'*'+data[col[k]][j]+'*'+data[col[k]][j]+first[i][12+danxishu_long*k]
                elif(first[i][9+danxishu_long*k:12+danxishu_long*k]=='**1'):
                    shi=shi+str(int(first[i][0+danxishu_long*k:8+danxishu_long*k], 2))+'*'+data[col[k]][j]+'*1'+first[i][12+danxishu_long*k]
#                    最后一组要另外处理
            if(first[i][9+danxishu_long*(bianlianggeshu-1):]=='**2'):
                shi=shi+str(int(first[i][0+danxishu_long*(bianlianggeshu-1):8+danxishu_long*(bianlianggeshu-1)], 2))+'*'+data[col[bianlianggeshu-1]][j]+'*'+data[col[bianlianggeshu-1]][j]
            elif(first[i][9+danxishu_long*(bianlianggeshu-1):]=='**1'):
                shi=shi+str(int(first[i][0+danxishu_long*(bianlianggeshu-1):8+danxishu_long*(bianlianggeshu-1)], 2))+'*'+data[col[bianlianggeshu-1]][j]+'*1'
           
            bds[i].append(shi)
    return bds

    # shi=data.x1[j]+first[i][0:3]
#
##------------------求出对应表达式的值-------------------------------------------

def qiuzhi(bds):
    bds_value=[[]for i in range(sumzhongqun)]
   
    for i in range(sumzhongqun):
        for j in range(len(data[col[0]])):
            exspression = bds[i][j]
            Calculator = InversPolishCalculator()
            ret = Calculator.deal(exspression)
            ret = float(ret)
            bds_value[i].append(ret)
    return bds_value
#print(type(bds_value[0][0]))竟然输出class ‘str’,要转换类型
#
##----生成没一个表达式的种群并且计算每一个种群中每一个个体的数学表达式的值---------
#       
##-------------------------求适应度---------------------------------------------

def qiushiyingdu(bds_value):
    fitness=[]
    for i in range(sumzhongqun):
        fit=0
        pingfanghe=0
        for j in range(len(data[col[0]])):
            pingfanghe = pingfanghe+(bds_value[i][j]-data[col[len(col)-1]][j])**2
        fit=pingfanghe/sumzhongqun
        fit=round(fit,2)
        fitness.append(fit)
    return fitness


def zuiyoubiaodashi(first):
    bianlianggeshu=len(col)-1
    shi=''
#            代码优化
    for k in range(bianlianggeshu-1):#a***2+b***2+c***2每六个算是一个系数最后一组除外

        if(first[9+danxishu_long*k:12+danxishu_long*k]=='**2'):#a***2+a***2+a***2每六个算是一个系数最后一组除外
            shi=shi+str(int(first[0+danxishu_long*k:8+danxishu_long*k], 2))+'*'+col[k]+'^2'+first[12+danxishu_long*k]
        elif(first[9+danxishu_long*k:12+danxishu_long*k]=='**1'):
            shi=shi+str(int(first[0+danxishu_long*k:8+danxishu_long*k], 2))+'*'+col[k]+first[12+danxishu_long*k]
#                    最后一组要另外处理
    if(first[9+danxishu_long*(bianlianggeshu-1):]=='**2'):
        shi=shi+str(int(first[0+danxishu_long*(bianlianggeshu-1):8+danxishu_long*(bianlianggeshu-1)], 2))+'*'+col[bianlianggeshu-1]+'^2'
    elif(first[9+danxishu_long*(bianlianggeshu-1):]=='**1'):
        shi=shi+str(int(first[0+danxishu_long*(bianlianggeshu-1):8+danxishu_long*(bianlianggeshu-1)], 2))+'*'+col[bianlianggeshu-1]
   
    return shi

newzhongqun = copy.deepcopy(first)
bds=dairubiaodashi(first)#先让代码能够跑起来
bds_value=qiuzhi(bds)
fitness=qiushiyingdu(bds_value)
childmostfitness.append(min(fitness))
most_value=min(fitness)
most_fitness_change.append(most_value)
most_fit=first[fitness.index(min(fitness))]
most_bdss.append(most_fit)
look_most_bdss.append(zuiyoubiaodashi(most_fit))
most_bds_value=bds_value[fitness.index(min(fitness))]
#
#
##轮盘选择
def lunpanxuanze(first):
    max_fitness = int(max(fitness))
    min_fitness = int(min(fitness))
    newzhongqun=[]
    for i in range(sumzhongqun):
        if(len(newzhongqun)==200):
            break
        for j in range(sumzhongqun):
            if(len(newzhongqun)==200):
                break
            fit = random.randint(min_fitness,max_fitness)
            if(fitness[j]<fit):
                xuanzhong=first[j]
                newzhongqun.append(xuanzhong)
                if(len(newzhongqun)==200):
                    break
    return newzhongqun
#
##交叉
#
def jiaocha():
    for i in range(sumzhongqun):
        tab=random.random()
        if(tab<jiaochagailv):
# print('进行交叉',i)
            min=random.randint(0,(len(col)-1)*danxishu_long-2)#染色体长度
            max=random.randint(0,(len(col)-1)*danxishu_long-2)
            j=random.randint(0,199)
           
            t=min
            if(min>max):
                min=max
                max=t
            if(min==0 and max==(len(col)-1)*danxishu_long-2):
                max=(len(col)-1)*danxishu_long-2-1
            copy_i = newzhongqun[i][:]
            copy_j = newzhongqun[j][:]
            stri=newzhongqun[i][min:max]
            strj=newzhongqun[j][min:max]
            if(min!=0):
                newzhongqun[i]=newzhongqun[i][0:min]+strj+newzhongqun[i][max:]
                newzhongqun[j]=newzhongqun[j][0:min]+stri+newzhongqun[j][max:]
            elif(min==0):
                newzhongqun[i]=strj+newzhongqun[i][max:]
                newzhongqun[j]=stri+newzhongqun[j][max:]
                
#                防止交叉出现0并使用系数交换
            for n in range(len(col)-1):
                if(str(int(newzhongqun[i][0+danxishu_long*n:8+danxishu_long*n], 2))=='0' or str(int(newzhongqun[j][0+danxishu_long*n:8+danxishu_long*n], 2))=='0'):
                    newzhongqun[i] = copy_i
                    newzhongqun[j] = copy_j
                    xishujiaohuan=random.randint(0,len(col)-1-1)
                    min=0+danxishu_long*xishujiaohuan
                    max=8+danxishu_long*xishujiaohuan
                    stri=newzhongqun[i][min:max]
                    strj=newzhongqun[j][min:max]
                    if(min!=0):
                        newzhongqun[i]=newzhongqun[i][0:min]+strj+newzhongqun[i][max:]
                        newzhongqun[j]=newzhongqun[j][0:min]+stri+newzhongqun[j][max:]
                    elif(min==0):
                        newzhongqun[i]=strj+newzhongqun[i][max:]
                        newzhongqun[j]=stri+newzhongqun[j][max:]
    return newzhongqun
#
#
##变异
def bianyi():
    for i in range(sumzhongqun):
        tab=random.random()
        if(tab<bianyigailv):
# print('进行变异',i)
            bianyiweizhi=random.randint(0,(len(col)-1)*danxishu_long-2)
#            if(bianyiweizhi==0 or bianyiweizhi==6 or bianyiweizhi==12):#系数变异
            if(bianyiweizhi%danxishu_long<=7):
                b=str(random.randint(1,50))
                b_2=format(int(b),'08b')
                if(bianyiweizhi<=7):
                    newzhongqun[i]=b_2+newzhongqun[i][8:]
                else:
                    newzhongqun[i]=newzhongqun[i][0:int(bianyiweizhi/danxishu_long)*danxishu_long]+b_2+newzhongqun[i][int(bianyiweizhi/danxishu_long)*danxishu_long+8:]
#            elif(bianyiweizhi==5 or bianyiweizhi==11):
            elif(bianyiweizhi%danxishu_long==12):
                b=suanshu[random.randint(0,3)]
                newzhongqun[i]=newzhongqun[i][0:bianyiweizhi]+b+newzhongqun[i][bianyiweizhi+1:]
#            elif(bianyiweizhi==2 or bianyiweizhi==3 or bianyiweizhi==4):#可以利用数学公式求出，但这里太少就直接判断
            elif(bianyiweizhi%danxishu_long==9 or bianyiweizhi%danxishu_long==10 or bianyiweizhi%danxishu_long==11):
                cifang=random.randint(1,2)
                if(bianyiweizhi<(len(col)-1)*danxishu_long-2-2):
                    if(cifang==1):
                        b='**1'
                        newzhongqun[i]=newzhongqun[i][0:9+int(bianyiweizhi/danxishu_long)*danxishu_long]+b+newzhongqun[i][12+int(bianyiweizhi/danxishu_long)*danxishu_long:]
                    else:
                        b='**2'
    #                    newzhongqun[i]=newzhongqun[i][0:2]+b+newzhongqun[i][5:]
                        newzhongqun[i]=newzhongqun[i][0:9+int(bianyiweizhi/danxishu_long)*danxishu_long]+b+newzhongqun[i][12+int(bianyiweizhi/danxishu_long)*danxishu_long:]
                else:     
                    if(cifang==1):
                        b='**1'
                        newzhongqun[i]=newzhongqun[i][0:(len(col)-1)*danxishu_long-2-2]+b
                    else:
                        b='**2'
                        newzhongqun[i]=newzhongqun[i][0:(len(col)-1)*danxishu_long-2-2]+b
                
    return newzhongqun
#
#
dai=0
bian =0
for i in range(diedaishu):
    if(i<100):
        weigaibian=40
    elif(i<300):
        weigaibian=30
    elif(i<500):
        weigaibian=20
    else:
        weigaibian=10
    newzhongqun=lunpanxuanze(newzhongqun)
    newzhongqun= jiaocha()
    newzhongqun = bianyi()
    bds=dairubiaodashi(newzhongqun)
    bds_value=qiuzhi(bds)
    fitness=qiushiyingdu(bds_value)
    childmostfitness.append(min(fitness))
    if(min(fitness)<most_value):
        most_value=min(fitness)
        most_fitness_change.append(most_value)
        most_fit=newzhongqun[fitness.index(min(fitness))]
        most_bdss.append(most_fit)
        look_most_bdss.append(zuiyoubiaodashi(most_fit))
        most_bds_value=bds_value[fitness.index(min(fitness))]
        dai=i
        bian=0
    else:
        most_fitness_change.append(most_value)
#    print('表达式的y值：',most_bds_value)
    
    print('第',i+1,'代：')
    print('最优解的变化：')
    print(look_most_bdss)
    print('本代最优解',zuiyoubiaodashi(newzhongqun[fitness.index(min(fitness))]))
    print('本代最优适应度',min(fitness))
# print(childmostfitness)
    print('目前为止最优的解',zuiyoubiaodashi(most_fit))
    print('目前为止最优的解的适应度(MSE)',most_value)
#    优化下一代的种群
    if(most_value==0):
        break
    bian=bian+1
    if(bian>=weigaibian):
        print('超过',weigaibian,'次未改变最优种群')
        newzhongqun=[]
        for j in range(sumzhongqun):
            newzhongqun.append(most_bdss[j%len(most_bdss)])
shi=zuiyoubiaodashi(most_fit)
print('======================================================================')
print('在第',dai+1,'有最优的表达式：')
print(shi)
print('适应度(越小越优)：')
print(most_value)

duibi = pd.DataFrame({'实际y':data[col[len(col)-1]],'预测y':most_bds_value}, columns=['实际y','预测y'])
print(duibi)