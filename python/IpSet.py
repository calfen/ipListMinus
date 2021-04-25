'''
Created on Jan 22, 2021
authuor: calfen

'''
import ipaddress
# import sys
# import pydoc
# import copy
import unittest
# from ipaddress import IPv4Network
# from netrc import netrc
# from builtins import str


class IpList(object):

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.ipList == other.ipList

    @property
    def ipList(self):
        return self._ipList

    @ipList.setter
    def ipList(self, inString):
        print(inString)
        print('1')
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

    @property
    def startEndFormat(self):
        __ipList = self.ipList
        startIp, endIp = __ipList[0][0], __ipList[0][-1]
        __ipStringList = []
        for i in range(len(__ipList) - 1):
            if __ipList[i+1][0] == endIp + 1:
                endIp = __ipList[i+1][-1]
            else:
                __ipStringList.add(str(startIp) + '-' + str(endIp))
                startIp, endIp = __ipList[i+1][0], __ipList[i+1][-1]
        __ipStringList.append(str(startIp) + '-' + str(endIp))
        return __ipStringList

    @property
    def is_legal(self):
        try:
            assert len(self.__ipStringList) <= 2,  '地址不合法'
            if len(self.__ipStringList) == 1:
                ipaddress.ip_network(self.__ipStringList[0])
            else:
                for ip in self.__ipStringList:
                    ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    def overlaps(self, other):
        return 0
        return 1
        return -1
        pass

    def __add__(self, other):
        # print(self.ipList)
        IpList._ipList = [ipAddr for ipAddr in ipaddress.collapse_addresses(
            self.ipList + other.ipList)]
        return IpList()

    def minus(self, other):
        pass


class test_IpList(unittest.TestCase):

    ipTest = [IpList() for i in range(10)]
    ipTest[0].ipList = '192.168.1.0/16'
    ipTest[1].ipList = '192.168.0.0/16'
    ipTest[2].ipList = '192.168.1.0/24'
    ipTest[3].ipList = '192.168.2.0/24'
    ipTest[4].ipList = '192.168.1.0-192.168.1.255'
    ipTest[5].ipList = '192.168.1.0-192.168.1.155'
    ipTest5String = ['192.168.1.0/25', '192.168.1.128/28',
                     '192.168.1.144/29', '192.168.1.152/30']
    ipTest[6].ipList = '192.168.2.0-192.168.2.255'
    ipTest[7].ipList = '192.168.1.0-192.168.2.255'

    def test_is_legal(self):
        self.assertFalse(self.ipTest[0].is_legal)
        self.assertTrue(self.ipTest[1].is_legal)
        self.assertTrue(self.ipTest[5].is_legal)

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
