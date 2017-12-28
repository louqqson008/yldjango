# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-11-24
# @version : 1.3.0


import sys,time,requests
sys.path.append('../')
from yltestplatform.PO import BasePage,PublicPage,LogPage,readConfig
from yltestplatform.Data import PoAllData

globalreadconfig = readConfig.ReadConfig()

base_api_load = BasePage.ylAPI()
base_sql_load = BasePage.YlfinMysql()


#申请小贷方法
#向ini配置文件写入贷款appl_id
def load_appl_record(headers):
    try:
        appl_record = base_api_load.post_api(PoAllData.LOAD_APPL_API,PoAllData.LOAD_APPL_VALUE,headers)
        if PublicPage.api_check_ack(appl_record) == True:
            print (appl_record['data']['applId'],type(appl_record['data']['applId']))
            globalreadconfig.set_testdata_ini('testLoad','load_appl_id',appl_record['data']['applId'])
            #print ('===>贷款申请成功')
            LogPage.debug_log('===>贷款申请成功')
        else:
            #print ('贷款申请失败：' + appl_record['message'])
            LogPage.debug_log('贷款申请失败：' + appl_record['message'])
    except Exception as e:
        LogPage.error_log(e)
        raise e
    return appl_record

#globalreadconfig = readConfig.ReadConfig()
#通过获取ini配置中心的appl_id，进行初审领取
def load_cs_lq():
    try:
        for i in range(20):
            #初始化全局变量TESTLOADAPPL
            TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
            CS_TJ = "SELECT RISK_SCORE,APPL_STATUS FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
            CS_LOAD_SQL = "UPDATE jinfu_loan_pro.fp_loan_appl SET APPL_STATUS = '04',TRIAL_USER_ID = 'UM0000000016' WHERE APPL_ID = '%s'"%TESTLOADAPPL
            cstj = base_sql_load.sql_select(CS_TJ)
            #print (TESTLOADAPPL)
            if isinstance(cstj,list):
                if cstj[0]['APPL_STATUS'] == '00' or cstj[0]['APPL_STATUS'] == '04':
                    if cstj[0]['RISK_SCORE'] == None:
                        #print ('未获得风控评分，等待%s分钟'%(i))
                        LogPage.debug_log('未获得风控评分，等待%s分钟'%(i))
                        time.sleep(60)
                    else:
                        base_sql_load.sql_update(CS_LOAD_SQL)
                        #print ('===>初审领取成功')
                        LogPage.debug_log('===>初审领取成功')
                        break
                else:
                    #print ('订单：' + TESTLOADAPPL + '状态不是未领取，不可直接改数据库')
                    LogPage.debug_log('订单：' + TESTLOADAPPL + '状态不是未领取，不可直接改数据库')
                    break
            else:
                #print (TESTLOADAPPL + '订单不是初审未领取的单子')
                LogPage.debug_log(TESTLOADAPPL + '订单不是初审未领取的单子')
                break
    except Exception as e:
        LogPage.error_log(e)
        raise e

#通过获取ini配置中心的appl_id，进行终审领取
def load_zs_lq():
    try:
        TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
        ZS_TJ = "SELECT APPL_STATUS FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
        ZS_LOAD_SQL = "UPDATE jinfu_loan_pro.fp_loan_appl SET APPL_STATUS = '05',REVIEW_USER_ID = 'UM0000000016' WHERE APPL_ID = '%s'"%TESTLOADAPPL
        zstj = base_sql_load.sql_select(ZS_TJ)
        if isinstance(zstj,list):
            if zstj[0]['APPL_STATUS'] == '01' or zstj[0]['APPL_STATUS'] == '05':
                base_sql_load.sql_update(ZS_LOAD_SQL)
                #print ('===>终审领取成功')
                LogPage.debug_log('===>终审领取成功')
            else:
                #print ('订单：' + TESTLOADAPPL + '状态不是终审未领取，不可直接改数据库')
                LogPage.debug_log('订单：' + TESTLOADAPPL + '状态不是终审未领取，不可直接改数据库')
    except Exception as e:
        raise e


#初审审批方法load_cs_sp
def load_cs_sp(headers):
    try:
        TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
        LOAD_CS_VALUE = {"loanAmt":"%s"%PoAllData.TESTLOADAMT,"reason":"111","loanAmount":"0.00","loanNum":"0","repayMonth":"0.00","remark":"",
                        "auditStatus":"ADVISE_PASS","period":"12","applId":"%s"%TESTLOADAPPL,"temp":False}
        #审批前进入审批页面
        #cssptj = base_api_load.get_code_api(PoAllData.LOAD_CS_TJ,newheaders)
        #cssptj = 200
        cssp = base_api_load.post_api(PoAllData.LOAD_CS_API,LOAD_CS_VALUE,headers)
        #print (cssp)
        if PublicPage.api_check_ack(cssp) == True:
            #print ('===>初审审批成功')
            LogPage.debug_log('===>初审审批成功')
        else:
            LogPage.error_log('====>初审审批异常：' + cssp['message'])
    except Exception as e:
        raise e

#终审审批方法load_zs_sp()
def load_zs_sp(headers):
    try:
        TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
        LOAD_ZS_VALUE = {"loanAmt":"%s"%PoAllData.TESTLOADAMT,"reason":"111","remark":"","auditStatus":"SUCCEED","period":"12","financeSourceId":"1",
        "applId":"%s"%TESTLOADAPPL,"temp":False}
        #cssptj = base_api_load.get_code_api(PoAllData.LOAD_CS_TJ,newheaders)
        #cssptj = 200
        zssp = base_api_load.post_api(PoAllData.LOAD_ZS_API,LOAD_ZS_VALUE,headers)
        #print (zssp)
        if PublicPage.api_check_ack(zssp) == True:
            #print ('===>终审审批成功')
            LogPage.debug_log('===>终审审批成功')
        else:
            LogPage.error_log(zssp['message'])
    except Exception as e:
        raise e

#用户签约并提款方法
def load_signing_qy(headers):
    try:
        TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
        QY_TYPE_API = "https://yltest.xylpay.com/loan-web/contract/pending/list?applId=%s"%TESTLOADAPPL
        #合同的类型，新合同模版
        contract_type = base_api_load.get_api(QY_TYPE_API,headers)
        #print (contract_type)
        LOAN_QY_SQL = "SELECT FUND_CODE,BANK_CARD_ID FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
        loan_qy = base_sql_load.sql_select(LOAN_QY_SQL)
        #print (TESTLOADAPPL,loan_qy)
        #资金端校验
        if loan_qy[0]['FUND_CODE'] == 'OWN':
            LOAD_SSQ_API = "https://yltest.xylpay.com/loan-web/contract/get?bizId=%s&type=%s"%(TESTLOADAPPL,contract_type['data'][0]['type'])
            ssqurl = base_api_load.get_api(LOAD_SSQ_API,headers)
            #print (ssqurl)
            #进入上上签页面是否成功
            if PublicPage.api_check_ack(ssqurl) == True:
                #print (loan_qy[0]['BANK_CARD_ID'],type(loan_qy[0]['BANK_CARD_ID']))
                LOAD_QYCG_VALUE = {"applId":"%s"%TESTLOADAPPL,"cardId":int("%s"%loan_qy[0]['BANK_CARD_ID'])}
                #print (LOAD_QYCG_VALUE['cardId'],type(LOAD_QYCG_VALUE['cardId']))
                qycg = base_api_load.post_api(PoAllData.LOAD_QYCG_API,LOAD_QYCG_VALUE,headers)
                #print (qycg)
                #签约成功接口 是否调用成功
                if PublicPage.api_check_ack(qycg) == True:
                    #print  ('===>自有资金：用户签约成功')
                    LogPage.debug_log('===>自有资金：用户签约成功')
                else:
                    LogPage.error_log('===>自有资金：用户签约失败' + qycg['message'])
            else:
                LogPage.error_log('打开上上签页面错误：'+ ssqurl['message'])

        elif loan_qy[0]['FUND_CODE'] == 'JINFU':
            #print (type(TESTLOADAPPL),type(contract_type['data'][0]['type']))
            LOAD_SSQ_API = "https://yltest.xylpay.com/loan-web/contract/get?bizId=%s&type=%s"%(TESTLOADAPPL,contract_type['data'][0]['type'])
            ssqurl = base_api_load.get_api(LOAD_SSQ_API,headers)
            print (ssqurl)
            if PublicPage.api_check_ack(ssqurl) == True:
                LOAD_QYCG_VALUE = {"applId":"%s"%TESTLOADAPPL,"cardId":int("%s"%loan_qy[0]['BANK_CARD_ID'])}
                qycg = base_api_load.post_api(PoAllData.LOAD_QYCG_API,LOAD_QYCG_VALUE,headers)
                #print (qycg)
                if PublicPage.api_check_ack(qycg) == True:
                    #print  ('===>金服资金：用户签约成功')
                    LogPage.debug_log('===>金服资金：用户签约成功')

                else:
                    print ('===>金服资金：用户签约失败' + qycg['message'])
            else:
                print ('打开上上签页面错误：'+ ssqurl['message'])
        else:
            print ("非自由资金、金服资金，不支持自动签约")
            if TESTLOADAPPL:
                DEL_SQL = "DELETE  FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
                base_sql_load.sql_delete(DEL_SQL)
            else:
                pass
    except Exception as e:
        raise e


def load_dtl_fkcg():
    try:
        TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')
        DTL_START = "SELECT TRANSFER_STAT,LOAN_STAT,LOAN_ID FROM jinfu_loan_pro.fp_loan_dtl WHERE APPL_ID = '%s'"%TESTLOADAPPL
        dtl_value = base_sql_load.sql_select(DTL_START)
        print (dtl_value)
        for i in range(10):
            #print (i,type(i))
            if dtl_value[0]['TRANSFER_STAT'] == '02' and dtl_value[0]['LOAN_STAT'] == '01':
                #print ("===>订单：" + TESTLOADAPPL +"放款成功" )
                LogPage.debug_log("===>订单：" + TESTLOADAPPL +"放款成功")
                #print (dtl_value[0]['LOAN_ID'])
                globalreadconfig.set_testdata_ini('testLoad','load_loan_id',dtl_value[0]['LOAN_ID'])
                break
            else:
                LogPage.debug_log("========>等待订单：" + TESTLOADAPPL + "放款第%s分钟"%i)
                time.sleep(60)
                if i == 9:
                    LogPage.debug_log('10分钟没有放款，算放款失败')
                    break
    except Exception as e:
        raise e


#PublicPage.login_api()
#time.sleep(5)
#new_headers = PublicPage.take_new_headers()
#time.sleep(5)
#appl_record = base_api_load.post_api(PoAllData.LOAD_APPL_API,PoAllData.LOAD_APPL_VALUE,new_headers)
#print  (appl_record['data']['applId'])
#globalreadconfig.set_testdata_ini('load_appl',appl_record['data']['applId'])
#load_appl_record(new_headers)
#time.sleep(5)
#PublicPage.ht_login_api()

#TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl')
#FUND_BANK_SQL = "SELECT FUND_CODE,BANK_CARD_ID FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
#fund_bank = base_sql_load.sql_select(FUND_BANK_SQL)
#print (fund_bank)
#TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl')

#print (LOAD_SSQ)
#load_signing_qy()

'''
PublicPage.login_api()
newheaders = PublicPage.take_new_headers()
PublicPage.ht_login_api()
htnewheaders = PublicPage.ht_take_new_headers()

load_appl_record(newheaders)
load_cs_lq()
load_cs_sp(htnewheaders)
load_zs_lq()
load_zs_sp(htnewheaders)
'''
