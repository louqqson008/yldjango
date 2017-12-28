# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-11-24
# @version : 1.3.1

import sys,time,requests,xlrd
#import logging
sys.path.append('../')
from yltestplatform.PO import BasePage,LogPage,readConfig
from yltestplatform.Data import PoAllData

globalreadconfig = readConfig.ReadConfig()
base_api_load = BasePage.ylAPI()
base_sql_load = BasePage.YlfinMysql()


#--------------------------------调试新方法---------------------------------------------

#logging.basicConfig(level=logging.WARNING,
#                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

#--------------------------------调试新方法---------------------------------------------


#用户注册功能
def register_api():
    try:
        is_user =base_sql_load.sql_select(PoAllData.SEL_MOBILE_SQL)
        if isinstance(is_user,list):
            print ('====>用户已存在,不进行注册操作')
        else:
            mobile_register = base_api_load.get_api(PoAllData.MOBILE_REGISTER_CODE_API,PoAllData.HEADERS_OLD)
            if api_check_ack(mobile_register) == True:
                mobile_check = base_api_load.get_api(PoAllData.MOBILE_REGISTER_CHECK_API,PoAllData.HEADERS_OLD)
                if api_check_ack(mobile_check) == True:
                    is_register = base_api_load.post_api(PoAllData.USER_REGISTER_API,PoAllData.USER_REGISTER_VALUE,PoAllData.HEADERS_OLD)
                    if api_check_ack(is_register) == True:
                        print ('=======>' + is_register['message'])
                    else:
                        print ('=======>' + is_register['message'])
                else:
                    print ('=======>' + mobile_check['message'])
    except Exception as e:
        raise e


#用户登录
def login_api():
    try:
        results = base_api_load.post_api(PoAllData.LOGIN_API,PoAllData.LOGIN_VALUE,PoAllData.HEADERS_OLD)
        #print (results)
        #print (type(results['data']['token']))
        if api_check_ack(results) == True:
            globalreadconfig.set_testdata_ini('testData','token',results['data']['token'])
            globalreadconfig.set_testdata_ini('testData','userid',results['data']['userId'])
            #print (results['data']['userId'])
            print ('===>掌柜登录成功')
            LogPage.debug_log('===>掌柜登录成功')
        elif results['code'] == None:
            print ('登录接口为None')
        else:
            print (results['message'])
    except Exception as e:
        LogPage.error_log(e)
    return results

#获取登录后带token的header
def take_new_headers():
    try:
        newtoken = globalreadconfig.get_ini_testdata('token')
        #print (newtoken)
        PoAllData.HEADERS_OLD['token'] = newtoken
    except Exception as e:
        LogPage.error_log(e)
    return PoAllData.HEADERS_OLD

#后台管理员登录
def ht_login_api():
    try:
        #获取短信验证码
        results = base_api_load.post_api(PoAllData.HT_LOGIN_API,PoAllData.HT_MOBILE,PoAllData.HT_HEADERS)
        #用户实际登录接口，和上面的接口为同一个，传的值不同
        results = base_api_load.post_api(PoAllData.HT_LOGIN_API,PoAllData.HT_VALUE,PoAllData.HT_HEADERS)
        #print (results)
        if api_check_ack(results) == True:
            globalreadconfig.set_testdata_ini('testData','ht_token',results['data']['token'])
            print ('===>后台登录成功')
            LogPage.debug_log('===>后台登录成功')
        else:
            print (results['message'])
    except Exception as e:
        LogPage.error_log(e)
    return results

#获取后台header
def ht_take_new_headers():
    try:
        newtoken = globalreadconfig.get_ini_testdata('ht_token')
        #print (newtoken)
        PoAllData.HT_HEADERS['token'] = newtoken
    except Exception as e:
        raise e
        LogPage.error_log(e)
    return PoAllData.HT_HEADERS



#从xlse中获取用例
def get_loan_xlsx():
    case_list = []
    #book获得excel的对象
    #sheetname 获得sheet名称
    #loan_sheet  通过sheet名值得对应sheet对象
    try:
        xlsx = xlrd.open_workbook('../Data/LoanCase.xlsx')
        sheetname = xlsx.sheet_names()[0]
        loan_sheet = xlsx.sheet_by_name(sheetname)
        #rows  获取行数
        rows = loan_sheet.nrows
        for i in range(rows - 1):
            row_values = loan_sheet.row_values(i + 1)
            #print (row_values,type(row_values))
            case_list.append(row_values)
        print (case_list,type(case_list))
        return case_list
    except Exception as e:
        LogPage.error_log(e)


# 接口返回ACK方法
def api_check_ack(par):
    par = par['code']
    if par == 'ACK':
        return True
    else:
        return False
