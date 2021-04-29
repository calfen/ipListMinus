import argparse
import string
from IpList import IpList
from ipMinus import doExcel

def main():
    parser = argparse.ArgumentParser(description="IP地址处理工具")
    parser.add_argument("-s", type=str, help="输入一个ip字符串")
    parser.add_argument("-f", type=str, help="输入excel文件地址")
    args = parser.parse_args()
    if args.f is not None:
        doExcel(args.f)
    elif args.s is not None:
#         print(args.s)
        ipL = IpList()
        ipL.setByString(args.s)
        ipL.printStartEndFormat()
        ipL.printCommonFormat()
    else:
        parser.print_help()
        
#     parser.add_argument("-e", help = "给出一个excel，两个列表相减")
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument("echo", help = "东方啦经理都发生了飞机撒的风景")
#     args = parser.parse_args()
#     print(args.echo)
# parser = argparse.ArgumentParser(description="IP地址处理工具")
# parser.add_argument("pString", type=str, help="输入一个ip字符串")
main()