# -*- coding: UTF-8 -*-
from configparser import ConfigParser
import pymysql

config = ConfigParser()
config.read("config.ini")


host = config.get("mysql","host")
port = int(config.get("mysql","port"))
user = config.get("mysql","user")
passwd = config.get("mysql","password")
db = config.get("mysql","db_name")
class sqlDeviceMpa:
    # 获取数据库命令对象
    connect = None
    cursor = None

    def __init__(self):
        self.openDatabase()

    def test_conn(self):
        try:
            self.connect.ping()
        except:
            global connect, cursor
            # 打开数据库连接
            self.connect = pymysql.Connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                db=db,
                charset='utf8'
            )
            # 获取游标
            self.cursor = self.connect.cursor()

    def openDatabase(self):
        global connect, cursor
        # 打开数据库连接
        self.connect = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.connect.cursor()

    # 检查设备ID
    def checkData(self, code, deviceid):
        self.test_conn()
        sql = "SELECT * FROM  device_map WHERE code='{}'".format(code)
        self.cursor.execute(sql)
        sqlRes = self.cursor.fetchone()
        if sqlRes == None:
            return False
        sqlCode = sqlRes[0]
        sqlDeviceId = sqlRes[1]
        if deviceid == "" or deviceid == None:
            return False
        if sqlDeviceId == None or sqlDeviceId == "":
            self.updateData(code,deviceid)
            return True
        return check_device.check_id_device(sqlDeviceId,deviceid)

    # 如果查询出来的设备ID为空则更新设备ID
    def updateData(self,code,deviceid):
        self.test_conn()
        sql = " UPDATE device_map SET deviceid = '{}' WHERE code = '{}' ".format(deviceid,code)
        self.cursor.execute(sql)
        self.connect.commit()

    def insertCode(self,listCode):
        self.test_conn()
        if listCode == None:
            return False
        sql = "INSERT INTO device_map (code) VALUES ('{}')"
        for i in listCode:
            self.cursor.execute(sql.format(i))
            self.connect.commit()
        return True

    def getNotUsedCode(self):
        self.test_conn()
        sql = "SELECT * FROM  device_map WHERE deviceid = '' or deviceid is null "
        self.cursor.execute(sql)
        sqlRes = self.cursor.fetchall()
        listCode = []
        for i in sqlRes:
            listCode.append(i[0])
        return listCode

    def getUsedCode(self):
        self.test_conn()
        sql = "SELECT * FROM  device_map WHERE deviceid !='' or deviceid is not null and LENGTH(trim(deviceid))>0"
        self.cursor.execute(sql)
        sqlRes = self.cursor.fetchall()
        return sqlRes