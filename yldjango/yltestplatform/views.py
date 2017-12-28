from django.shortcuts import render
from django.http import HttpResponse

import sys,unittest,time,os
import HTMLTestRunner
#sys.path.append('..')
from yltestplatform.PO import BasePage,PublicPage,LoanPage,PayPage
from yltestplatform.Data import PoAllData
#import PO.BasePage,PO.PublicPage,PO.LoanPage,PO.PayPage
#import Data.PoAllData


# Create your views here.
def index(request):
    #return HttpResponse("HELLO Django")
    return render (request,'index.html')

def login_action(request):
    return render (request,'login.html')



def yltest_action(request):

    if request.method == 'GET':
        PublicPage.login_api()
        new_headers = PublicPage.take_new_headers()
        #掌柜登录进行贷款申请操作
        time.sleep(5)
        LoanPage.load_appl_record(new_headers)
        time.sleep(5)

def yltest_submit(request):
        pass
