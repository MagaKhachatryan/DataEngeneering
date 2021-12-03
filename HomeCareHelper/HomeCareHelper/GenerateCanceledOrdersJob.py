from Job import Job as j
from datetime import datetime as dt
from datetime import timedelta
import pandas.io.sql as psql
import pandas as pd
import psycopg2
import random
import decimal

class GenerateCanceledOrdersJob(j):
    RepeatInterval=None
    ConnStr=None
    def __init__(self,interval,connstr):
        self.RepeatInterval = interval
        self.ConnStr=connstr

    def ExecuteJob(self):
         count=5
         conn = psycopg2.connect(self.ConnStr)
         randomCustomers=self.__GetRandomIdList(conn,"Customer",count)

         cur = conn.cursor()
         command = "select Company_Worker_Id,Company_Service_Id from Company_Worker_Company_Service"
         df = psql.read_sql(command, conn)

         workersIdList=df["company_worker_id"].tolist()
         servicesIdList=df["company_service_id"].tolist()
         indexList=[random.randrange(0, len(workersIdList)-1, 1) for i in range(count)]

         randomWorkers=[]
         randomServices=[]
         for ind in indexList:
            randomWorkers.append(workersIdList[ind])
            randomServices.append(servicesIdList[ind])

         registrationDate=dt.now()
         registrationDateList=[registrationDate] * count
         minutesAdded = timedelta(minutes = 5)
         doneDate=registrationDate+minutesAdded
         doneDateList=[doneDate] * count

         randomCurrencies=self.__GetRandomIdList(conn,"Currency",count)
         priceList= [random.randrange(1000, 200000, 1) for i in range(count)]
         priceList=[round(decimal.Decimal(x),2) for x in priceList]

         values=[]
         i=0
         while i<count:
            values.append((randomCustomers[i],randomWorkers[i],randomServices[i],
                          0,registrationDateList[i],doneDateList[i],False,randomCurrencies[i],priceList[i]))
            i=i+1

         sql = "INSERT INTO Orders(customer_id,company_worker_id,company_service_id,state,registerDate,doneDate,isGraded,currency_Id,price)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
         cur=conn.cursor()
         cur.executemany(sql,values)
         conn.commit()
         conn.close()

    def __GetRandomIdList(self,conn,tableName,count):
        cur = conn.cursor()
        command = "select Id from " + tableName + ' ;'
        df = psql.read_sql(command, conn)
        objList = df['id'].tolist()
        indexList=[random.randrange(0, len(objList)-1, 1) for i in range(count)]
        randomObjList=[]
        for ind in indexList:
            randomObjList.append(objList[ind])
        return randomObjList