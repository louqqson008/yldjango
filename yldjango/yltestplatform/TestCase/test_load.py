# -*- coding:utf-8 -*-
#!/usr/local/bin/python3

import sys,unittest,time,os
import HTMLTestRunner
sys.path.append('../')
from PO import BasePage,PublicPage,LoanPage,PayPage
from Data import PoAllData


class LoanTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        print ('------>执行用例成功')

    def test_01(self):

        #用户注册
        #PublicPage.register_api()
        PublicPage.login_api()
        new_headers = PublicPage.take_new_headers()
        #掌柜登录进行贷款申请操作
        time.sleep(5)
        LoanPage.load_appl_record(new_headers)
        time.sleep(5)

        #后台管理员登录，进行初审领取、初审、终审领取、终审
        PublicPage.ht_login_api()
        time.sleep(5)
        #'''
        ht_new_headers = PublicPage.ht_take_new_headers()
        LoanPage.load_cs_lq()
        LoanPage.load_cs_sp(ht_new_headers)
        time.sleep(2)
        LoanPage.load_zs_lq()
        LoanPage.load_zs_sp(ht_new_headers)
        time.sleep(2)
        #'''


    def test_02(self):
        PublicPage.login_api()
        new_headers = PublicPage.take_new_headers()
        #用户签约返款，放款成功
        LoanPage.load_signing_qy(new_headers)
        LoanPage.load_dtl_fkcg()
        time.sleep(2)
        #还款
        PayPage.pay_all(new_headers)


if __name__ == '__main__':

    #unittest.main()

    testunit = unittest.TestSuite()
    testunit.addTest(LoanTest("test_01"))
    testunit.addTest(LoanTest("test_02"))
    nowtime = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    now = time.strftime("%H%M%S",time.localtime(time.time()))
    if not os.path.exists('../Result/' + nowtime):
        os.mkdir('../Result/' + nowtime)
    else:
        pass
    fp=open('../Result/'+nowtime+'/'+"result"+now +".html",'wb')
    runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title='小贷自动化流程用例',description=u'result:')
    runner.run(testunit)
    fp.close()
