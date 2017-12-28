# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-11-24
# @version : 1.3.1


import  pymysql,requests,pymongo
from pymongo import MongoClient
import  time,sys,json
import  stomp
sys.path.append('../')
#import readConfig
from yltestplatform.PO import readConfig,LogPage

globalreadconfig = readConfig.ReadConfig()


#-------------------------------------------------
#BasePage总说明：包含mysql、mq 类
#所有类都以yl开头，其他所有方法都不会使用，保证类的唯一性
#
#-------------------------------------------------


class ylAPI:

    def __init__(self):
        self.timeout = 10


    def get_api(self,url,headers):
        try:
            ylget = requests.get(url,headers=headers,timeout=self.timeout)
            if ylget.status_code == 200:
                result = ylget.json()
                return result
            else:
                #print ('GET接口调用失败:' + ylget.status_code  + ':' + url)
                LogPage.error_log('GET接口调用失败:' + ylget.status_code  + ':' + url)
        except Exception as e:
            raise

    def get_value_api(self,url,params,headers):
        try:
            ylget = requests.get(url,params=params,headers=headers,timeout=self.timeout)
            if ylget.status_code == 200:
                result = ylget.json()
                return result
            else:
                #print ('GET接口调用失败:' + ylget.status_code  + ':' + url)
                LogPage.error_log('GET接口调用失败:' + ylget.status_code  + ':' + url)
        except Exception as e:
            raise

    def get_code_api(self,url,headers):
        try:
            ylget = requests.get(url,headers=headers,timeout=self.timeout)
            if ylget.status_code == requests.codes.ok:
                #print ("get接口链接成功%s"%url)
                LogPage.debug_log("get接口链接成功%s"%url)
                return ylget.status_code
            else:
                #print ("接口链接失败%s"%url)
                LogPage.error_log("接口链接失败%s"%url)
            #value = ylget.status_code
        except Exception as e:
            raise

    def post_api(self,url,data,headers):
        try:
            if isinstance(data,str):
                #print (json.dumps(data))
                data = eval(data)
                ylpost = requests.post(url,data=json.dumps(data),headers=headers,timeout=self.timeout)
                value = ylpost.text()
                return (value)
            elif isinstance(data,(int,list,dict)):
                #print (json.dumps(data))
                ylpost = requests.post(url,data=json.dumps(data),headers=headers,timeout=self.timeout)
                if ylpost.status_code == 200:
                    value = ylpost.json()
                    return (value)
                else:
                    #print ('POST接口调用失败:' + ylpost.status_code + ':' + url)
                    LogPage.error_log('POST接口调用失败:' + ylget.status_code  + ':' + url)
            else:
                #print ("data不是int,list,dict类型，类型不对")
                LogPage.error_log("data不是int,list,dict类型，类型不对")
        except Exception as e:
            raise


class YlfinMysql:

    try:
        conn = pymysql.connect(
            host=globalreadconfig.get_ini_mysql("host"),
            port=int(globalreadconfig.get_ini_mysql("port")),
            user=globalreadconfig.get_ini_mysql("user"),
            passwd=globalreadconfig.get_ini_mysql("passwd"),
            db=globalreadconfig.get_ini_mysql("db"),
            cursorclass=pymysql.cursors.DictCursor
        )
        dbcur = conn.cursor()
        #print ("数据库链接成功")
    except Exception as e:
        raise

    def __init__(self):
        pass
    #-------------------------------------------------
    #执行select语句
    #-------------------------------------------------
    def sql_select(self,sql):
        self.sql = sql
        try:
            self.dbcur.execute(sql)
            dbdata = self.dbcur.fetchall()
            if not isinstance(dbdata,list):
                #print ('在数据库中未搜索到内容' + sql)
                LogPage.error_log('在数据库中未搜索到内容' + sql)
            else:
                return dbdata
            #print (dbdata)
        except Exception as e:
            raise e

    #-------------------------------------------------
    #可执行Update，Insert语句
    #-------------------------------------------------
    def sql_update(self, sql):
        self.sql = sql
        try:
            self.dbcur.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise e


    #--------------------------------------------------
    #执行delete删除语句
    #-------------------------------------------------
    def sql_delete(self,sql):
        self.sql = sql
        try:
            self.dbcur.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise e

    #-------------------------------------------------
    #用例中不再进行SQL操作时，关闭SQL
    #-------------------------------------------------
    def sql_close(self):
        #关闭对象
        self.dbcur.close()
        #关闭与数据库链接
        self.conn.close()
        print ('已关闭数据库')


#—------------------------------------------------
#监听器
#—------------------------------------------------
class MyListener(object):
    def on_error(self, headers, message):
        #print('received an error %s' % message)
        LogPage.debug_log('received an error %s' % message)
    def on_message(self, headers, message):
        #print('received a message %s' % message)
        LogPage.debug_log('received an error %s' % message)

#—------------------------------------------------
# 作用：连接MQ，获取MQ信息  及   发送信息给MQ
#—------------------------------------------------
class YlfinMq:

    def __init__(self):
        pass

    #—------------------------------------------------
    #连接上MQ功能
    #—------------------------------------------------
    def mq_conn(self):
        global conn
        mqhost = globalreadconfig.get_ini_mq("host")
        mqport = globalreadconfig.get_ini_mq("port")
        try:
            conn = stomp.Connection10([(mqhost,mqport)])
            conn.set_listener('',MyListener)
            conn.start()
            conn.connect()
            print('MQ链接成功')
        except Exception as e:
            raise e

    #—------------------------------------------------
    #mq获取信息：  队列还是主题根据path
    #—------------------------------------------------
    def mq_sub(self,mqpath):
        self.mqpath = mqpath
        try:
            conn.subscribe(destination=mqpath,id=1,ack='auto')
            time.sleep(3)
            sub = conn.disconnect()
            return sub
            #print('获取MQ信息成功')
            LogPage.debug_log('获取MQ信息成功')
        except Exception as e:
            raise e

    #—------------------------------------------------
    #mq发送信息：  队列还是主题根据path
    #—------------------------------------------------
    def mq_send(self,mqpath,mqvalue):
        self.mqpath = mqpath
        self.mqvalue = mqvalue
        try:
            conn.send(body=mqvalue,destination=mqpath)
            time.sleep(3)
            conn.disconnect()
            #print(str('发送MQ：%s信息成功')%mqvalue)
            LogPage.debug_log(str('发送MQ：%s信息成功')%mqvalue)
        except Exception as e:
            raise e

#
#Mongodb封装类
#使用方式如下：
#nn = YlfinMongo()
#aa= nn.mongo_onekeyfind('user',username='13085060209')
#
class YlfinMongo:

    def __init__ (self):
        pass

    try:
            #链接客户端
        moconn = MongoClient(globalreadconfig.get_ini_monogo("ipurl"),int(globalreadconfig.get_ini_monogo("port")))
            #db = moconn.get_database("QAusercenter")
            #db.auth('usercenter', 'usercenter')
            #连接mongo数据库
        dbmongo = moconn.usercenter
        monuser = globalreadconfig.get_ini_monogo("user")
            #print (monuser)
        monpw = globalreadconfig.get_ini_monogo("pw")
            #通过帐号密码获取操作权限
        if monuser == None and monpw == None:
            #print ('没有账号密码链接mongo')
            LogPage.debug_log('没有账号密码链接mongo')
        else:
            dbmongo.authenticate(monuser,monpw)
            #colltest = dbmongo['Collections']
        #print (dbmongo)
        #print ("链接Mongo成功")

    except Exception as e:
        raise e

    #添加单条记录
    def mongo_insert(self,sheet,invalue):
        self.sheet = sheet
        self.invalue = invalue
        try:
            mon = mongo_client.sheet
            mon.insert(invalue)
        except Exception as e:
            raise e

    #添加多条记录
    def mongo_insert_many(self,sheet,manyvalue):
        self.sheet = sheet
        self.manyvalue = manyvalue
        try:
            mon = mongo_client.sheet
            mon.insert_many(manyvalue)
        except Exception as e:
            raise e

    def mongo_onekeyfind(self,sheet,**kwargs):
        self.sheet = sheet
        if sheet == 'user':
            try:
                keyfind = self.dbmongo.user.find(kwargs)
                #print (kwargs)
                return keyfind
            except Exception as e:
                raise e
        elif sheet == 'store':
            try:
                keyfind = self.dbmongo.store.find(kwargs)
                #print (kwargs)
                return keyfind
            except Exception as e:
                raise e

class YlfinFtp:

    def __init__ (self):
        pass



class YlfinRedis:

    def __init__ (self):
        pass
