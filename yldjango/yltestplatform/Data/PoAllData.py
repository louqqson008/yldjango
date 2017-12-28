# -*- coding:utf-8 -*-
#!/usr/local/bin/python3


# 本文件都为全局变量，
#包含：接口API地址
#包含：数据库SQL语句
#

import sys,time,requests
sys.path.append('../')
from yltestplatform.PO import readConfig,BasePage

globalreadconfig = readConfig.ReadConfig()

TESTMOBILE = globalreadconfig.get_ini_fixeddata("mobile")
TESTLOADAMT = globalreadconfig.get_ini_fixeddata("amount")
TESTPRODUCT = globalreadconfig.get_ini_fixeddata("product")
TESTLOADAPPL = globalreadconfig.get_ini_testload('load_appl_id')

TESTPAYPW = '96e79218965eb72c92a549dd5a330112'
TESTGPS = "29.95076,121.478735"



#----------------------------------------------API-----------------------------------------------------------------

#注册短信发送
MOBILE_REGISTER_CODE_API = "https://yltest.xylpay.com/jinfu/web/register/mobile/code?mobile=%s&type=REGISTER"%TESTMOBILE
#注册短信验证
MOBILE_REGISTER_CHECK_API = "https://yltest.xylpay.com/jinfu/web/register/mobile/confirm?&type=REGISTER&verifyCode=000000&mobile=%s"%TESTMOBILE
#添加银行卡短信验证
MOBILE_BANKCARD_CODE_API = "https://yltest.xylpay.com/jinfu/web/register/mobile/code?&mobile=%s&type=BANKCARD"%TESTMOBILE
#设置支付密码的短信验证码
MOBILE_PAY_PW_API ="https://yltest.xylpay.com/cashier-web/web/dealerpassword/verifycode?mobile=%s"%TESTMOBILE


#注册接口
USER_REGISTER_API = "https://yltest.xylpay.com/jinfu/web/shopkeeper/auth/register"
USER_REGISTER_VALUE = {"content":{"gps":TESTGPS},"mobile":TESTMOBILE,"newPassword":"e10adc3949ba59abbe56e057f20f883e","verifyCode":"000000"}



#登录接口和参数值
LOGIN_API = "https://yltest.xylpay.com/jinfu/web/shopkeeper/auth/login"
LOGIN_VALUE =  {"password":"e10adc3949ba59abbe56e057f20f883e","content":{"udid":"","virtual":"","vpn":"","mac":"","gps":"32.094513,118.684564","ip":""},"userName":TESTMOBILE}
HEADERS_OLD = {
    'Content-Type': "application/json",
    'user-agent': "ylzg-QA/2.9.1 (iPhone; iOS 10.2.1; Scale/2.00)",
    'ga-latitude': "32.094513",
    'ga-longitude': "118.684564",
    }

#后台管理员登录接口和参数
HT_LOGIN_API = "http://yltest.xylpay.com/jinfu-mgt-srv/web/auth/login"
HT_MOBILE = {"loginId": "test16", "password": "96e79218965eb72c92a549dd5a330112"}
HT_VALUE = {"loginId": "test16", "password": "96e79218965eb72c92a549dd5a330112", "verificationCode": "000000"}
HT_HEADERS = {
    'content-type': "application/json",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }



#实名认证接口
#USER_CERTIFY_API = "https://yltest.xylpay.com/jinfu/web/shopkeeper/user/certify"
#USER_CERTIFY_VALUE = {}
#接口传图片太烦，直接改数据库
USER_CERTIFY_SQL = "UPDATE jinfu_user_pro.user_inf SET ID_CARD_NO = '610502199011906028' AND USER_NAME = '专用帐号董旋' AND IDENTITY_AUTH = '1' WHERE MOBILE = '%s'"%TESTMOBILE









#贷款申请接口
LOAD_APPL_API = "https://yltest.xylpay.com/jinfu/web/loan/apply/start"
LOAD_APPL_VALUE = {"termLen":"12","productId":TESTPRODUCT,"applAmt":int(TESTLOADAMT)}

#初审审批接口
LOAD_CS_TJ = "http://yltest.xylpay.com/jinfu-mgt/web/loan/user/fin?userId=UC0000026446&applId=302140560706601043&v=1512464352400"
LOAD_CS_API = "http://yltest.xylpay.com/jinfu-mgt/web/loan/audit/trial"
LOAD_CS_VALUE = {"loanAmt":"%s"%TESTLOADAMT,"reason":"111","loanAmount":"0.00","loanNum":"0","repayMonth":"0.00","remark":"","auditStatus":"ADVISE_PASS","period":"12",
                "applId":"%s"%TESTLOADAPPL,"temp":False,"relationship":"OTHER"}


#终审审批接口
LOAD_ZS_API = "http://yltest.xylpay.com/jinfu-mgt/web/loan/audit/review"
LOAD_ZS_VALUE = {"loanAmt":"%s"%TESTLOADAMT,"reason":"111","remark":"","auditStatus":"SUCCEED","period":"12","financeSourceId":"1","relationship":"OTHER","applId":"%s"%TESTLOADAPPL,"temp":False}
        #{"loanAmt":"10000","reason":"111","remark":"","auditStatus":"SUCCEED","period":"12","financeSourceId":"1","relationship":"OTHER","applId":"302142146160212000","temp":false}


#跳转到上上签接口
LOAD_SSQ_API = "https://yltest.xylpay.com/jinfu/web/loan/contract/bestSignContract?applyId=%s&pc=false"%TESTLOADAPPL

#签约成功接口
LOAD_QYCG_API = "https://yltest.xylpay.com/jinfu/web/loan/agree"




#还款接口
#获取需要还款的金额
LOAN_CALC_API = "https://yltest.xylpay.com/jinfu/web/loan/calc/start"

#实际还款接口
LOAN_REPAY_API = "https://yltest.xylpay.com/jinfu/web/loan/repay/start"

#预付接口，获取支付方式，校验是否已设置支付密码
LOAN_PREPAY_API = "https://yltest.xylpay.com/cashier-web/web/v2/prepay"


#设置支付密码验证码校验
PAYPW_MOB_CHECK_API = "https://yltest.xylpay.com/cashier-web/web/dealerpassword/checkUserInfo"
PAYPW_MOB_CHECK_VALUE = {"verifyCode":"000000","mobile":"%s"%TESTMOBILE}

PAYPW_SET_API = "https://yltest.xylpay.com/cashier-web/web/dealpassword"
#支付密码默认：111111
PAYPW_SET_VALUE = {"password":"%s"%TESTPAYPW,"verifyCode":"000000","password2":"%s"%TESTPAYPW,"mobile":"%s"%TESTMOBILE}

#支付接口
PAY_API = "https://yltest.xylpay.com/cashier-web/web/pay"

#----------------------------------------------SQL-----------------------------------------------

#搜索手机号是否存在
SEL_MOBILE_SQL = "SELECT USER_ID FROM jinfu_user_pro.user_inf WHERE  MOBILE = %s"%TESTMOBILE

#通过手机号查贷款申请记录
MOBLOE_SQL_LOAD_APPL = "SELECT * FROM jinfu_loan_pro.fp_loan_appl as A LEFT JOIN jinfu_user_pro.user_inf as B ON B.USER_ID = A.USER_ID WHERE B.MOBILE = %s"%TESTMOBILE

#初审条件，有分控评分
CS_TJ = "SELECT RISK_SCORE FROM jinfu_loan_pro.fp_loan_appl WHERE APPL_ID = '%s'"%TESTLOADAPPL
#初审领取updta sql
CS_LOAD_SQL = "UPDATE jinfu_loan_pro.fp_loan_appl SET APPL_STATUS = '04',TRIAL_USER_ID = 'UM0000000013' WHERE APPL_ID = '%s'"%TESTLOADAPPL
#终审领取updata sql
ZS_LOAD_SQL = "UPDATE jinfu_loan_pro.fp_loan_appl SET APPL_STATUS = '05',REVIEW_USER_ID = 'UM0000000013' WHERE APPL_ID = '%s'"%TESTLOADAPPL


#aa = testsql.sql_select(SEL_LOAD_APPL)
#print (aa)
