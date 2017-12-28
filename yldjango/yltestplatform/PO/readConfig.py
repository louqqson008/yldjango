# -*- coding:utf-8 -*-
#!/usr/local/bin/python3

import  configparser

class ReadConfig:

    def __init__(self):
        self.config = configparser.ConfigParser()

    #获取  节MysqlConfig   key = name 的value值
    def get_ini_mysql(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("MysqlConfig",name)
        except Exception as e:
            raise
        return value

    #获取  节MqConfig   key = name 的value值
    def get_ini_mq(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("MqConfig",name)
        except Exception as e:
            raise
        return value

    #获取  节MonogoConfig   key = name 的value值
    def get_ini_monogo(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("MonogoConfig",name)
        except Exception as e:
            raise
        return value

    def get_ini_fixeddata(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("testFixedData",name)
        except Exception as e:
            raise
        return value

    def get_ini_testdata(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("testData",name)
        except Exception as e:
            raise e
        return value

    def get_ini_testload(self,name):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            value = self.config.get("testLoad",name)
        except Exception as e:
            raise e
        return value

    #新建ini文件的   节jd    key   以及 token=value值
    #用户登录后，将token值插入到ini中
    def set_testdata_ini(self,jd,key,value):
        self.config.read('yltestplatform/config.ini',encoding='UTF-8')
        try:
            #添加新的节
            #config.add_section(self.top)
            self.config.set(jd,key,value)
            opini = open('yltestplatform/config.ini', "w+")
            self.config.write(opini)
            opini.close()
            #print ('ini添加成功')
        except Exception as e:
            raise e
