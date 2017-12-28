# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-12-13



import sys,time,requests
sys.path.append('../')
from yltestplatform.PO import BasePage,PublicPage,LogPage,readConfig
from yltestplatform.Data import PoAllData

globalreadconfig = readConfig.ReadConfig()

base_api_load = BasePage.ylAPI()
base_sql_load = BasePage.YlfinMysql()




def pay_current():
    pass

#全部还款，内置支付密码设置
def pay_all(headers):
    TESTLOANID = globalreadconfig.get_ini_testload('load_loan_id')
    TESTAMOUNT = globalreadconfig.get_ini_fixeddata('amount')
    LOAN_REPAY_VALUE = {"amt":"%s"%TESTAMOUNT,"couponIds":[],"repayType":"PRE_ALL","loanId":"%s"%TESTLOANID,"periods":[],"expected":0.0}
    repay_re = base_api_load.post_api(PoAllData.LOAN_REPAY_API,LOAN_REPAY_VALUE,headers)
    #print (repay_re)
    try:
        if PublicPage.api_check_ack(repay_re) == True:
            PREPAY_VALUE = repay_re['data']
            prepay_re = base_api_load.post_api(PoAllData.LOAN_PREPAY_API,PREPAY_VALUE,headers)
            if PublicPage.api_check_ack(prepay_re) == True:
                LogPage.debug_log('===>成功进入收银台页面')
                #把payOrderNo写入的ini配置中心
                PAY_ORDER_NO = prepay_re['data']['payOrderNo']
                #支付密码校验与设置
                if prepay_re['data']['dealPasswordExists'] == True:
                    LogPage.debug_log('已设置支付密码，进行还款操作:====>')
                    PAY_VALUE = {"dealPassword":"%s"%PoAllData.TESTPAYPW,"cardId":100276,"payId":"DEBIT_CARD_TRANSFER","payOrderNo":"%s"%PAY_ORDER_NO}
                    pay = base_api_load.post_api(PoAllData.PAY_API,PAY_VALUE,headers)
                    if PublicPage.api_check_ack(pay) == True:
                        LogPage.debug_log('==========================>' + pay['message'])
                    else:
                        LogPage.debug_log(pay['message'])
                else:
                    LogPage.debug_log('未设置支付密码，先进行设置支付密码操作：====>')
                    paypw_mobile = base_api_load.get_api(PoAllData.MOBILE_PAY_PW_API,headers)
                    #设置支付密码，短信获取
                    if PublicPage.api_check_ack(paypw_mobile) == True:
                        pay_mob_check = base_api_load.post_api(PoAllData.PAYPW_MOB_CHECK_API,PoAllData.PAYPW_MOB_CHECK_VALUE,headers)
                        if pay_mob_check['code'] == 'USER_OR_DPWD_NOT_EXIST':
                            LogPage.debug_log('------>进入设置密码页面')
                            set_pay_pw = base_api_load.post_api(PoAllData.PAYPW_SET_API,PoAllData.PAYPW_SET_VALUE,headers)
                            if PublicPage.api_check_ack(set_pay_pw) == True:
                                LogPage.debug_log('支付密码设置成功，进行还款操作=======>')
                                PAY_VALUE = {"dealPassword":"%s"%PoAllData.TESTPAYPW,"cardId":100276,"payId":"DEBIT_CARD_TRANSFER","payOrderNo":"%s"%PAY_ORDER_NO}
                                pay = base_api_load.post_api(PoAllData.PAY_API,PAY_VALUE,headers)
                                if PublicPage.api_check_ack(pay) == True:
                                    LogPage.debug_log('==========================>' + pay['message'])
                                else:
                                    #print (pay['message'])
                                    LogPage.debug_log(pay['message'])
                    else:
                        LogPage.debug_log('---->设置支付密码获取短信验证失败')

        #调用确认按钮时，提示已有一笔还款记录，需要15分钟才能继续
        elif '15' in repay_re['message']:
            LogPage.debug_log('===>后续功能：去还款详情页面进行还款')

        else:
            LogPage.debug_log('========>确认还款按钮，调用失败')
    except Exception as e:
        raise e
