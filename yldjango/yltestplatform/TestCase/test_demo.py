# -*- coding:utf-8 -*-
#!/usr/local/bin/python3

import sys,unittest,time
sys.path.append('../')
from PO import BasePage
import uuid,json
from time import strftime,gmtime



class CaseTestA(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #
        #初始化：把BasePage中的类   实例化
        #YlfinMysql  mysql数据库操作
        #YlfinMq（ip，port）     MQ 操作：参数  IP 和 port端口
        #
        self.sqlapi = BasePage.ylAPI()
        self.sqltest = BasePage.YlfinMysql()
        self.mqtest = BasePage.YlfinMq()
        self.mongotest = BasePage.YlfinMongo()
        self.redistest = BasePage.YlfinRedis()
        self.ftptest = BasePage.YlfinFtp()

    @classmethod
    def tearDownClass(self):
        print ('执行用例成功')

    def test_01(self):
        sqltest = self.sqltest
        mqtest = self.mqtest
        #申请日期  appl_dt
        appl_dt = strftime("%Y-%m-%d", gmtime())
        #申请编号 appl_id
        CaseTestA.appl_id = str(uuid.uuid1())
        userid =  'UC0000005166'
        traceid = 'b33e4120b2df44f5b5f7d810c24240ee'
        s_test = "{'applId':'%s','userId':'%s','traceId':'%s'}"%(CaseTestA.appl_id,userid,traceid)
        product_id = ['L01001','L01002','L01003','L01004','L01006','L01007']
        mqtest.mq_conn()
        mqtest.mq_send(s_test,'/queue/LOAN_IN_EYE')
        #执行模拟贷款申请的  insert 语句
        load_appl_sql = "INSERT INTO `jinfu_loan_pro`.`fp_loan_appl` (`APPL_ID`, `PRODUCT_ID`, `USER_ID`, `ACCT_NO`, `APPL_DT`, `SIGNED`, `APPL_STATUS`, \
        `APPL_MEMO`, `APPL_AMT`, `TRX_MEMO`, `BANK_CARD_ID`, `TERM_LEN`, `TERM_TYPE`, `APPR_AMT`, `APPR_TERM_LEN`, `APPR_SERVICE_FEE_MONTH_RT`, `REPAY_MODE`,\
        `LOAN_RT`, `LOAN_RT_TYPE`, `SERVICE_FEE_RT`, `SERVICE_FEE_MONTH_RT`, `CREDIT_LINE_RSRV_ID`, `USER_EXTRA`, `DEALER_USER_ID`, `DEALER_ID`,\
        `TRIAL_USER_ID`, `REVIEW_USER_ID`, `HANGUP`, `CHANNEL`, `FUND_AUDIT_STATUS`, `SIGN_TS`, `FUND_CODE`, `FINANCE_SOURCE_ID`, `TEST_SOURCE`, `GPS`,\
        `RISK_SCORE`, `LOAN_QUOTA`, `RISK_RESULT`, `CREATE_OPID`, `CREATE_TS`, `TRACE_ID`, `LAST_MNT_OPID`, `LAST_MNT_TS`, `VERSION_CT`, `import_tag`) \
        VALUES ('%s', 'L01001', '%s', '17081600000001', '%s', NULL, '12', NULL, '50000.00', NULL, NULL, '12', '3', NULL, NULL,\
        '0.00000000', '05', '0.02000000', 'MONTH', '0.00000000', '0.00000000', '17102500000001', NULL, NULL, NULL, 'UM0000000404', NULL, b'0', 'SELF', NULL, NULL, NULL, NULL, NULL, NULL,\
         '1.5', '0', '人工审核', 'UC0000005166', '2017-10-25 16:26:17.000000', 'af074c70c22b441caeab21b4c9b01c8b', 'system', '2017-10-31 10:12:50.000000', '16', '0')"%(CaseTestA.appl_id,userid,appl_dt)

        #upsql = "UPDATE `jinfu_user_pro`.`user_inf` SET `USER_ID`='UC0000002448', `MOBILE`='13655883315', `EMAIL`=NULL, `LOGIN_PWD`='ad0beb84c480405ea645bbdc8a9c4421', `DEAL_PWD`=NULL, `USER_NAME`='董璇2', `ID_CARD_NO`='610502199010016028', `STATUS`='NORMAL', `IDENTITY_AUTH`=b'1', `IDENTITY_AUTH_DATE`='2017-08-29 15:40:05', `STORE_AUTH`=b'1', `BANK_AUTH`=b'1', `CASHIER_FROZEN`=b'0', `SOURCE`='3', `SOURCE_NAME`=NULL, `AB_TEST`=NULL, `DEALER_USER_ID`=NULL, `CREATE_OPID`='system', `CREATE_TS`='2017-07-06 15:33:09', `LAST_MNT_OPID`='UC0000002448', `LAST_MNT_TS`='2017-08-29 15:40:05', `VERSION_CT`='13', `UUID`='f0b79b4f-caa8-438b-ba83-915ef14010ca', `import_tag`='0' WHERE (`USER_ID`='UC0000002448')";
        sqltest.sql_update(load_appl_sql)

        #selsql = "select * from jinfu_loan_pro.fp_loan_appl where APPL_ID = '111eee'"
        selsql = "select * from jinfu_loan_pro.fp_loan_appl where APPL_ID = '%s'"%CaseTestA.appl_id
        #print (selsql)
        insqltrue = sqltest.sql_select(selsql)
        print (insqltrue)
        if insqltrue:
            self.assertIsNotNone(insqltrue, msg='update数据成功插入的数据库')
        else:
            insqltrue = None
            self.assertIsNotNone(insqltrue, msg='数据库没有查到unpdate数据')

        sqltest.sql_close()



    def test_02(self):
        sqltest = self.sqltest
        mqtest = self.mqtest
        appl_id = CaseTestA.appl_id
        print ('完成CaseTestA.test_02')
        #print (appl_id)
        #eye_sql = "select a,b,c   from t_loan_pro where applid = '%s'"%appl_id
        #sqltest.sql_select(eye_sql)






if __name__ == '__main__':
    #添加测试集合
    unittest.main()

    '''
    test_suit = unittest.TestSuite()
    test_suit.addTests(map(CaseTestA,['test_01','test_02']))
    #可使用unittest.TextTestRunner()类的run方法来运行
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suit)

    fp = open(r'.\Result\report.html','wb')
    suite =unittest.TestLoader().loadTestsFromTestCase(TestCase)
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='TestReport',description=u'用例执行情况')
    runner.run(suite)
    fp.close()
    '''
