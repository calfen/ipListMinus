import xlrd
from IpList import IpList


def readExcelSingle(fileName, colNum, rowNum):
    '''
    读取1行Excel数据
    parameter: fileName 文件名
                colNum  从第几列读取
                rowNum  从第几行读取
    返回ip地址List

    '''
    try:
        workbook = xlrd.open_workbook(fileName)
    except Exception:
        print('文件找不到')
    sheet1 = workbook.sheet_by_index(0)
    ipAddress = []
    for rowIndex in range(rowNum - 1, sheet1.nrows):
        colIP = sheet1.cell_value(rowIndex, colNum - 1)
        if colIP != '':
            ipAddress.append(colIP)
    return ipAddress


fileName = '../test.xlsx'
ipStringListCenter = readExcelSingle(fileName, 1, 3)
ipStringListBranch = readExcelSingle(fileName, 3, 3)
ipObjListCenter = []
ipObjListBranch = []
for ipString in ipStringListCenter:
    ipObj = IpList()
    ipObj.setByString(ipString)
    ipObjListCenter.append(ipObj)
for ipString in ipStringListBranch:
    ipObj = IpList()
    ipObj.setByString(ipString)
    ipObjListBranch.append(ipObj)
    indexCenter = 0
for ipObjCenter in ipObjListCenter:
    lineNum = []
    indexBranch = 0
    conflictIpObj = IpList()
    for ipObjBranch in ipObjListBranch:
        if ipObjCenter.is_overlaps(ipObjBranch):
            conflictIpObj = conflictIpObj + ipObjBranch
#             ipObjBranch.printCommonFormat()
            lineNum.append(indexBranch)
        indexBranch += 1
#     print('ok')
#     conflictIpObj.printCommonFormat()
#     conflictIpObj.printStartEndFormat()
#     print(lineNum)
    if len(lineNum) > 0:
        newIpObj = IpList()
        newIpObj = ipObjCenter - conflictIpObj
        print('总部的第' + str(indexCenter + 3) + '行: ' +
              ipStringListCenter[indexCenter] + ' 和:')
        for i in lineNum:
            print('分支第' + str(i + 3) + '行: 冲突' + ipStringListBranch[i])
        if newIpObj.ipList == []:
            print('应删除')
        else:
            print('应改为:')
            newIpObj.printCommonFormat()
            print('或改为:')
            newIpObj.printStartEndFormat()

    indexCenter += 1


# [print(ipObj.ipList) for ipObj in ipObjListCenter]
# [print(ipObj.ipList) for ipObj in ipObjListBranch]
# print(centerIpObjList)
# [print(ipObj.ipList) for ipObj in centerIpObjList]
