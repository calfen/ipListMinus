'''
Created on Jan 22, 2021
authuor: calfen

'''
import ipaddress
import copy
import unittest

class IpList(object):
    '''
    
    '''
    def __init__(self):
        self._ipList = []

    def __eq__(self, other):
        return self.ipList == other.ipList

    @property
    def ipList(self):
        return self._ipList

    @ipList.setter
    def ipList(self, inIpList):
        self._ipList = copy.copy(sorted(inIpList))
        
    def setByString(self, inString):
        self.__ipStringList = inString.split('-')
        if self.is_legal:
            if len(self.__ipStringList) == 1:
                self._ipList = [ipaddress.ip_network(self.__ipStringList[0])]
            else:
                self._ipList = list(ipaddress.summarize_address_range(
                    ipaddress.IPv4Address(self.__ipStringList[0]),
                    ipaddress.IPv4Address(self.__ipStringList[1])))
        else:
            self._ipList = []

    @property
    def commonFormat(self):
        return [str(ip) for ip in self.ipList]
    
    def printCommonFormat(self):
        if len(self.ipList) > 0:
            [print(str(ip)) for ip in self.ipList]
        else:
            print(None)
#         l = ['192.168.1.0-192.168.1.255']
#         print('common')
#         ll = ['192.168.1.0-192.168.1.255']
#         print(''.join(ll))
#         return [str(ip) for ip in self.ipList]

    @property
    def startEndFormat(self):
        __ipList = self.ipList
        if __ipList == []:
            return None
        startIp, endIp = __ipList[0][0], __ipList[0][-1]
        __ipStringList = []
        for i in range(len(__ipList) - 1):
            if __ipList[i + 1][0] == endIp + 1:
                endIp = __ipList[i + 1][-1]
            else:
                __ipStringList.add(str(startIp) + '-' + str(endIp))
                startIp, endIp = __ipList[i + 1][0], __ipList[i + 1][-1]
        __ipStringList.append(str(startIp) + '-' + str(endIp))
        return __ipStringList
    
    def printStartEndFormat(self):
        if len(self.ipList) == 0:
            print(None)
            return
        __ipList = self.ipList
        if __ipList == []:
            print('None')
        startIp, endIp = __ipList[0][0], __ipList[0][-1]
        __ipStringList = []
        for i in range(len(__ipList) - 1):
            if __ipList[i + 1][0] == endIp + 1:
                endIp = __ipList[i + 1][-1]
            else:
                print(str(startIp) + '-' + str(endIp))
                startIp, endIp = __ipList[i + 1][0], __ipList[i + 1][-1]
        print(str(startIp) + '-' + str(endIp))

    @property
    def is_legal(self):
        try:
            assert len(self.__ipStringList) <= 2, '地址不合法'
            if len(self.__ipStringList) == 1:
                ipaddress.ip_network(self.__ipStringList[0])
            else:
                for ip in self.__ipStringList:
                    ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    def is_overlaps(self, other):
        __sign = False
        for ipNet1 in self.ipList:
            for ipNet2 in other.ipList:
                if ipNet1.overlaps(ipNet2):
                    __sign = True
        return __sign
    
    def findOverlaps(self, other):
            __ipNetList = []
            ipListOverlaps = IpList()
            for ipNet1 in self.ipList:
                for ipNet2 in other.ipList:
                    if ipNet1.subnet_of(ipNet2):
                        __ipNetList.append(ipNet1)
                    elif ipNet1.supernet_of(ipNet2):
                        __ipNetList.append(ipNet2)
            ipListOverlaps._ipList = __ipNetList
            return ipListOverlaps
                    
    def __add__(self, other):
        # print(self.ipList)
        addList = IpList()
        addList._ipList = sorted(list(ipaddress.collapse_addresses(
            self.ipList + other.ipList)))
        return addList

    def __sub__(self,other):
        def minusListNet(listNetA,listNetB):
            '''
            两个网络list相减，直到没有重复
            返回[相减后的网络list，用于递归
            '''    
            for netA in listNetA:
                for netB in listNetB:
                    if netA.overlaps(netB):
                        overlapsSign = 1
                        if netA.supernet_of(netB):
                            resultNetList = list(netA.address_exclude(netB))
                            listNetA.remove(netA)
                            listNetA = listNetA + resultNetList
                        elif netA.subnet_of(netB):
                            listNetA.remove(netA)
                        return [listNetA,1,netB]
            return [listNetA,0,None]
        minusObj = IpList()
        __listNetA = copy.copy(self.ipList)
        __listNetB = copy.copy(other.ipList)
        sign = 1
        minusList = []
        while sign != 0:
            i = minusListNet(__listNetA,__listNetB)
            sign = i[1]
            __listNetA = i[0]
            if i[2] != None:
                minusList.append(i[2])
        minusObj._ipList = sorted(__listNetA)
        return minusObj


class test_IpList(unittest.TestCase):

    ipTest = [IpList() for i in range(20)] 
    # 错误格式
    ipTest[0].setByString('192.168.1.0/16')
    ipTest[1].setByString('192.168.0.0/16')
    ipTest[2].setByString('192.168.1.0/24')
    ipTest[3].setByString('192.168.2.0/24')
    ipTest[4].setByString('192.168.1.0-192.168.1.255')
    ipTest[5].setByString('192.168.1.0-192.168.1.155')
    ipTest5String = ['192.168.1.0/25', '192.168.1.128/28',
                     '192.168.1.144/29', '192.168.1.152/30']
    ipTest[6].setByString('192.168.2.0-192.168.2.255')
    ipTest[7].setByString('192.168.1.0-192.168.2.255')
    ipTest[9].setByString('192.168.1.64-192.168.2.155')
    ipTest[10].setByString('192.168.1.0-192.168.1.63')
    ipTest[11].setByString('10.0.0.5-10.1.1.24')
#   
    def test_is_legal(self):
        self.assertFalse(self.ipTest[0].is_legal)
        self.assertTrue(self.ipTest[1].is_legal)
        self.assertTrue(self.ipTest[5].is_legal)
#  
    def test_ipList(self):
        self.assertEqual(self.ipTest[1].ipList,
                         [ipaddress.ip_network('192.168.0.0/16')])
        self.assertEqual(self.ipTest[2].ipList, self.ipTest[4].ipList)
  
    def test_commonFormat(self):
        self.assertEqual(self.ipTest[1].commonFormat, ['192.168.0.0/16'])
        self.assertEqual(self.ipTest[5].commonFormat, self.ipTest5String)
  
    def test_getStartEndFormat(self):
        self.assertEqual(self.ipTest[1].startEndFormat,
                         ['192.168.0.0-192.168.255.255'])
        self.assertEqual(self.ipTest[5].startEndFormat,
                         ['192.168.1.0-192.168.1.155'])
  
    def test_add(self):
        self.assertEqual(self.ipTest[4] + self.ipTest[6], self.ipTest[7])
        self.ipTest[8] = self.ipTest[4] + self.ipTest[6]
        self.assertEqual(self.ipTest[8].startEndFormat,
                         ['192.168.1.0-192.168.2.255'])
           
    def test__is_overlaps(self):
        self.assertTrue(self.ipTest[6].is_overlaps(self.ipTest[7]))
        self.assertTrue(self.ipTest[7].is_overlaps(self.ipTest[6]))
        self.assertFalse(self.ipTest[4].is_overlaps(self.ipTest[6]))
   
    def test_findOverlaps(self):
        self.assertEqual(self.ipTest[7].findOverlaps(self.ipTest[6]),self.ipTest[6])
          
    def test_sub(self):
        self.assertEqual(self.ipTest[7] - self.ipTest[6],self.ipTest[4])
        self.assertEqual((self.ipTest[5] - self.ipTest[9]).ipList,self.ipTest[10].ipList)
#         print((self.ipTest[7] - self.ipTest[6]).startEndFormat)
#         print(self.ipTest[11].ipList)
#         print((self.ipTest[5] - self.ipTest[9]).ipList)
#         print(self.ipTest[5].ipList)
#         ipObj=IpList()
#         ipObj.setByString('10.0.0.1-10.1.1.24')
#         print(ipObj.ipList)
    def test_printCommonFormat(self):
        (self.ipTest[7]- self.ipTest[9]).printCommonFormat()
        (self.ipTest[7]- self.ipTest[9]).printStartEndFormat()