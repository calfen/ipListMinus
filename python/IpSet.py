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


class IpSet(object):

    def __init__(self, ipString):
        self._ipString = ipString
        pass

    def is_legal(self):
        try:
            ipList = self._ipString.split('-')
            assert len(ipList) <= 2,  '地址不合法'
            if len(ipList) == 1:
                ipaddress.ip_network(self._ipString)
            else:
                for ip in ipList:
                    ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    def getIpSet(self):
        ipList = self._ipString.split('-')
        if len(ipList) == 1:
            return [ipaddress.ip_network(self._ipString)]
        else:
            return list(ipaddress.summarize_address_range(
                ipaddress.IPv4Address(ipList[0]),
                ipaddress.IPv4Address(ipList[1])))

    def getCommonFormat(self):
        pass

    def getStartEndFormat(self):
        pass

    def overlaps(self, other):
        return 0
        return 1
        return -1
        pass

    def add(self, other):
        pass

    def minus(self, other):
        pass


class test_IpList(unittest.TestCase):

    ipTest1 = IpSet('192.168.1.0/16')
    ipTest2 = IpSet('192.168.0.0/16')
    ipTest3 = IpSet('192.168.1.0-192.168.1.255')
    ipTest4 = IpSet('192.168.1.0-192.256.1.255')

    def test_is_legal(self):
        self.assertFalse(self.ipTest1.is_legal())
        self.assertTrue(self.ipTest2.is_legal())
        self.assertTrue(self.ipTest3.is_legal())
        self.assertFalse(self.ipTest4.is_legal())

    def test_getIpSet(self):
        self.assertEqual(self.ipTest2.getIpSet(),
                         [ipaddress.ip_network('192.168.0.0/16')])
        self.assertEqual(self.ipTest3.getIpSet(),
                         [ipaddress.ip_network('192.168.1.0/24')])
