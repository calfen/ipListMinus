'''
Created on Jan 22, 2021
authuor: calfen

'''
import ipaddress
import xlrd
import sys
import pydoc
import copy
import unittest
#from IPy import IP,IPSet
#from _ast import If
#from pickle import TRUE
from datetime import datetime
from ipaddress import IPv4Network
from netrc import netrc
from builtins import str

#from tkinter.constants import CENTER
"""
检查IP/netmask是否合法
"""

'''
def checkip(ip):
	try:
		return ipaddress.ip_address(ip)
	except ValueError:
		pass
	try:
		return ipaddress.ip_network(ip)
	except ValueError:
		pass
	raise ValueError('%s is not a valid IP address' % ip)
'''
'''

'''

class Ip(object):
	def __init__(self, ipString):
		self._ipString = ipString

	def stringToIpSet(self):
		'''
		判断一个ip地址合法
		@author: calfen
		'''
		try:
			if self._ipString.find('-') == -1:
				return [ipaddress.ip_network(self._ipString)]
			else:
				ipList = self._ipString.split('-')
				assert len(ipList) == 2, '不是两段地址'
				startIp = ipList[0]
				endIp = ipList[1]
				return list(ipaddress.summarize_address_range(ipaddress.IPv4Address(startIp),ipaddress.IPv4Address(endIp)))
		except ValueError as e:
			print(self._ipString,'地址不合法')
# 			raise ValueError('%s 地址不合法' %self._ipString)

			return None
			sys.exit(1)
# 			print(self._ipString,'地址不合法')
# 			print(e)
# 			return False

class test_Ip(unittest.TestCase):
	def test_init(self):
		ipTest = Ip('192.168.1.0/16')
		self.assertEqual(ipTest.stringToIpSet(), None)
# 		with self.assertRaises(ValueError):
# 			ipTest.stringToIpSet()

		ipTest = Ip('192.168.1.0/24')
# 		print(ipTest.stringToIpSet())
		self.assertEqual(ipTest.stringToIpSet(),[ipaddress.ip_network('192.168.1.0/24')])
		ipTestRange = Ip('192.168.1.0-192.168.1.255')
# 		print(ipTestRange.stringToIpSet())
		self.assertEqual(ipTestRange.stringToIpSet(), [ipaddress.ip_network('192.168.1.0/24')])


#
#
'''
判断一
'''
def is_ip(address):
	'''
	判断一个ip地址合法
	@author: calfen
	'''
	try:
		if address.find('-') == -1:
			ipaddress.ip_network(address)
			return True
		else:
			return True
	except ValueError as e:
		print(address,'地址不合法')
		print(e)
		return False

def rmDirtyIP(ipList):
    '''
    去除不合法ip
    List
    '''
    return [ip for ip in ipList if is_ip(ip)]
#
#     for ip in ipList:
#         if is_ip(ip):
#             pass
#         else:
#             ipList.remove(ip)


'''
def is_not_net(ip):
    try:
        ipaddress.ip_network(ip)
        return False
    except ValueError as e:
        print(ip,'地址不合法')
        return True

def netmask_to_bit_length(netmask):
    """
    >>> netmask_to_bit_length('255.255.255.0')
    24
    >>>
    """
    # 分割字符串格式的子网掩码为四段列表
    # 计算二进制字符串中 '1' 的个数
    # 转换各段子网掩码为二进制, 计算十进制
    return str(sum([bin(int(i)).count('1') for i in netmask.split('.')]))
'''
'''
def calcIP(ipStringA,ipStringB):
    try:
        ipNetB = ipaddress.ip_network(ipStringA)
        ipNetA = ipaddress.ip_network(ipStringB)
    except NetmaskValueError:
        print(ipNetA,ipNetB,'地址不合法')
    if ipNetA.num_addresses > ipNetB.num_addresses :
        bigIP = ipNetA
        smallIP = ipNetB
    else :
        bigIP = ipNetB
        smallIP = ipNetA
#s = ipaddress.ip_address('192.168.0.1')
    if bigIP.overlaps(smallIP) :
        newIP=bigIP.address_exclude(smallIP)
        print("冲突IP是：")
        print(bigIP,"和",smallIP)
        print("替换成：")
        for ip in newIP:
            print(ip)
    else:
#        print("没有冲突IP")
        pass
    return

'''
"""

读取2行Excel数据
给出文件名，第几列地址，第几行开始
返回ip地址List

"""
# def readExcelDouble(fileName,colNum1,colNum2,rowNum):
# #     workbook = xlrd.open_workbook(fileName)
#     sheet1 = workbook.sheet_by_index(0)
#     ipAddress = []
#     for rowIndex in range(rowNum -1 ,sheet1.nrows):
#         colIP = sheet1.cell_value(rowIndex,colNum1 - 1) + '/' + sheet1.cell_value(rowIndex,colNum2 - 1)
#         if colIP != '':
#             ipAddress.append(colIP)
#     return ipAddress
def printGoogleAdsense():
	advContent= '<script data-ad-client="ca-pub-5760567978162752" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'
	print(advContent)

'''
读取1行Excel数据
给出文件名，第几列地址，第几行开始
返回ip地址List

'''
def readExcelSingle(fileName,colNum,rowNum):
    workbook = xlrd.open_workbook(fileName)
    sheet1 = workbook.sheet_by_index(0)
    ipAddress = []
    for rowIndex in range(rowNum - 1,sheet1.nrows):
        colIP = sheet1.cell_value(rowIndex,colNum - 1)
        if colIP != '':
            ipAddress.append(colIP)
    return ipAddress



'''
Stringip to [IPv4Network]
'''
def strToNetworkList(inString):
	if inString.find('-') == -1:
		return [IPv4Network(inString)]
	else:
		ipRange = inString.split('-')
		return list(ipaddress.summarize_address_range(ipaddress.IPv4Address(ipRange[0]),ipaddress.IPv4Address(ipRange[1])))

def minusListNet(listNetA,listNetB):
    '''
    两个网络list相减，碰到重复停止
    返回[相减后的网络list,是否重叠】
    '''
    for netA in listNetA:
        for netB in listNetB:
            # print(netA)
            # print('减')
            # print(netB)
            if netA.overlaps(netB):
                overlapsSign = 1
                if netA.supernet_of(netB):
                    resultNetList = list(netA.address_exclude(netB))
                    listNetA.remove(netA)
                    listNetA = listNetA + resultNetList
                else:
                    listNetA.remove(netA)
                return [listNetA,1,netB]
                # print('重叠等于')
                # print(listNetA)
                # return [listNetA,1]
            # print('不重叠等于')
            # print(listNetA)
    return [listNetA,0,None]

def listNetMinusListNet(listNetA,listNetB):
    '''
    两个网络list递归相减直到结束
    返回相减后的网络list和被减的网络List
    '''
    sign = 1
    minusList = []
    while sign != 0:
        # print(listNetA)
        # print('minus')
        # print(listNetB)
        i = minusListNet(listNetA,listNetB)
        sign = i[1]
        listNetA = i[0]
        if i[2] != None:
        	minusList.append(i[2])
        # print('eques')
        # print(listNetA)
    return [listNetA,list(set(minusList))]



def printStartEndIp(ipNetworkList):
	'''
	打印开始结束的ip表，串起开始结束IP

	'''
	ipnetWorkStartip = ipNetworkList[0][0]
	ipnetWorkEndip = ipNetworkList[0][-1]
	for i in range(len(ipNetworkList)-1):
		if ipNetworkList[i + 1][0] == ipnetWorkEndip + 1:
			ipnetWorkEndip = ipNetworkList[i + 1][-1]
		else:
			print(str(ipnetWorkStartip) + '-' + str(ipnetWorkEndip))
			ipnetWorkStartip = ipNetworkList[i + 1][0]
			ipnetWorkEndip = ipNetworkList[i + 1][-1]
	print(str(ipnetWorkStartip) + '-' + str(ipnetWorkEndip))


def strListToNetworkListList(stringList):
    '''
    [StringIp] to [[IPv4Network],[IPv4Network,IPv4Network]....]
    '''
    networkList = []
    for ipString in stringList:
        a=datetime.now()
        networkList.append(strToNetworkList(ipString))
        b=datetime.now()
        if (b - a).seconds > 2:
            print('转换' + ipString)
            print(str((b - a).seconds) + '秒')
# 		print(networkList)
    return networkList

def listListNetToListNet(netListList):
    '''
    二维list的网络地址转换为一纬
    '''
    return [net for netList in netListList for net in netList]

def findIndexOf2DimensionalList(netAddress,twoDimensionalNetAddressList):
	'''
	找出字符串在二维数组里的第一维度位置
	找到返回位置，找不到返回-1

	'''
	for index in range(len(twoDimensionalNetAddressList)):
		if netAddress in twoDimensionalNetAddressList[index]:
			return index
	return -1

def printNetIndexAndValue(netAddressList,twoDimensionalList,strList):
	'''
	打印分支冲突IP


	'''
	colum = set()
	for netAddress in netAddressList:
		index = findIndexOf2DimensionalList(netAddress,twoDimensionalList)
		colum.add(index)
	columList = list(colum)
	for colIndex in columList:
		print('第',end='')
		print(colIndex+3,end='')
		print('行：',end='')
		print(strList[colIndex],end='')
		print(',',end='')
	print('冲突')


def doWork(fileName):
    '''
    按照总部减多次分支重新改写

    '''
    ipListCenter = readExcelSingle(fileName,1,3)
    ipListCenter=rmDirtyIP(ipListCenter)
    ipListBranch = readExcelSingle(fileName,3,3)
    ipListBranch=rmDirtyIP(ipListBranch)
    ipNetworkListListBranch = strListToNetworkListList(ipListBranch)
    ipNetworkListListCenter = strListToNetworkListList(ipListCenter)
    ipNetWorkListBranch = listListNetToListNet(ipNetworkListListBranch)
    centerIndex = 0
    for netListCenter in ipNetworkListListCenter:
        ipNetworkListCenter = copy.deepcopy(netListCenter)
        # print(ipNetworkListCenter)
        # print('-')
        # print(ipNetWorkListBranch)
        resultMiniusNetList = listNetMinusListNet(ipNetworkListCenter,ipNetWorkListBranch)
        # print('结果')
        # print(resultMiniusNetList)
        # print('原来：')
        # print(netListCenter)
        if resultMiniusNetList[0] == [] or resultMiniusNetList[0] == None:
            print('总部的第' + str(centerIndex + 3) + '行:' + ipListCenter[centerIndex] + ' 和分支',end='')
            printNetIndexAndValue(resultMiniusNetList[1],ipNetworkListListBranch,ipListBranch)
            print('应删除')
        else:
            if resultMiniusNetList[0] != netListCenter:
                print('总部的第' + str(centerIndex + 3) + '行: ' + ipListCenter[centerIndex]  + '和分支',end='')
                printNetIndexAndValue(resultMiniusNetList[1],ipNetworkListListBranch,ipListBranch)
                newCenterNet = sorted(resultMiniusNetList[0])
                print('应删除后改为:')
                for ipNet in newCenterNet:
                    print(ipNet)
                # print('或改为：')
                # for ipNet in resultMiniusNetList:
                    # print(ipNet.with_netmask)
                print('或改为：')
                printStartEndIp(newCenterNet)
            # else:
                # print('没有交集')
#                 print(resultMiniusNetList[1])
        centerIndex = centerIndex + 1



# fileName = str(sys.argv[1])
# # fileName = '/Users/zhoujiangang/Downloads/test.xlsx'
# # print('文件名：',fileName)
# doWork(fileName)
# # printGoogleAdsense()
