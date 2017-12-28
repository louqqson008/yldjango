# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-12-22


import sys,time,os
import logging
sys.path.append('../')



nowtime = time.strftime("%Y-%m-%d",time.localtime(time.time()))
now = time.strftime("%H%M%S",time.localtime(time.time()))
if not os.path.exists('yltestplatform/Result/' + nowtime):
    os.mkdir('yltestplatform/Result/' + nowtime)
else:
    pass
filename = 'yltestplatform/Result/' + nowtime + '/log' + now + '.log'


'''
DEBUG：详细的信息,通常只出现在诊断问题上
INFO：确认一切按预期运行
WARNING：一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”)。这个软件还能按预期工作。
ERROR：更严重的问题,软件没能执行一些功能
CRITICAL：一个严重的错误,这表明程序本身可能无法继续运行
'''


#logging.basicConfig(level = logging.DEBUG,
#                format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                filename = filename,
#                filemode = 'w'
#                )

def debug_log(message):
    # 设置ligging对象，并且设置对象等级
    logger = logging.getLogger('testlog')
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        #设置一个写入本文的Handler,并且设置等级
        #注：写入控制台的StreamHandler   写入日志的FileHandler
        logtxt = logging.FileHandler(filename,mode='w')
        logtxt.setLevel(logging.DEBUG)

        logcmd = logging.StreamHandler()
        logcmd.setLevel(logging.DEBUG)
        #设置输入格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        logtxt.setFormatter(formatter)
        logcmd.setFormatter(formatter)

        logger.addHandler(logtxt)
        logger.addHandler(logcmd)
    logger.debug(message)
    #logger.removeHandler(logtxt)


def error_log(message):
    # 设置ligging对象，并且设置对象等级
    logger = logging.getLogger('testlog')
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        #设置一个写入本文的Handler,并且设置等级
        #注：写入控制台的StreamHandler   写入日志的FileHandler
        logtxt = logging.FileHandler(filename,mode='w')
        logtxt.setLevel(logging.ERROR)

        #设置输入格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        logtxt.setFormatter(formatter)

        logger.addHandler(logtxt)
    logger.error(message)
    #logger.removeHandler(logtxt)
