# -* - coding: UTF-8 -* -
#! /usr/bin/python

"""最小编辑距离
@author:  段雨非<mailto:duanyufeichn@foxmail.com>
@date:    2016-3-9
@stu_num: 3115370071
@desc:    自然语言处理第一次作业
@version: Python 3.4.3
"""

import codecs

#读文件，文件中有若干行，每行两个字符串，中间用空格分隔
def readfile():
    file = codecs.open("file.txt")
    strlist = []
    while 1:
        line = file.readline()
        strlist.append(line.rstrip().split(' '))
        if not line:
            break
        pass
    file.close()
    return strlist[0:len(strlist)-1]

#插入/删除 cost=1
insCost = 1
delCost = 1

#替换操作cost=2
def subCost(p,q):
    if(p != q): 
        return 2
    return 0

#打印二维数组
def printe(dm):
    for e in dm:
        print(e)

def mindist(peer):
    #m×n数组
    m = len(peer[0])
    n = len(peer[1])
    dm = [([0] * (m)) for i in range(n)]

    for i in range(1,m):
        dm[0][i] = i*insCost
    for i in range(1,n):
        dm[i][0] = i*delCost
    #printe(dm)
    for i in range(1,n):
        for j in range(1,m):
            #print(str(i)+' '+str(j))
            cins = dm[i-1][j] + insCost
            csub = dm[i-1][j-1] + subCost(peer[0][j-1],peer[1][i-1])
            cdel = dm[i][j-1] + delCost
            dm[i][j] = min(cins,csub,cdel)
            #printe(dm)

    print('(%s)和(%s) 的最小编辑距离： %d'%(peer[0],peer[1],dm[n-1][m-1]))
    return

if __name__ == '__main__':

    strlist = readfile()
    #读文件，对文件中每行的两个字符串求最小编辑距离
    for peer in strlist:
    #peer = strlist[4]
        mindist(peer)

