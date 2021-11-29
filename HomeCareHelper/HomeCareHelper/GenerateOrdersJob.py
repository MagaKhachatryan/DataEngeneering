from Job import Job as j
from datetime import datetime as dt
from datetime import timedelta
import pandas.io.sql as psql
import pandas as pd
import psycopg2
import numpy as np


class GenerateOrdersJob(j):
    
    RepeatInterval=None
    ConnStr=None

    def __init__(self,interval,connstr):
        self.RepeatInterval = interval
        self.ConnStr=connstr

    def ExecuteJob(self):
         count=10         

         conn = psycopg2.connect(self.ConnStr)

         randomCustomers=self.__GetRandomIdList(conn,"Customer",count)

         randomCompany_Workers=self.__GetRandomIdList(conn,"Company_Worker",count)

         randomCompnay_Services=self.__GetRandomIdList(conn,"Company_Service",count)

         state=2
         stateList=[state] * count

         registrationDate=dt.now()
         registrationDateList=[registrationDate] * count

         minutesAdded = timedelta(minutes = 1)
         doneDate=registrationDate+minutesAdded
         doneDate=doneDate.strftime("%m/%d/%y/%h/%m")
         doneDateList=[doneDate] * count


         isGraded=[False] * count

         randomCurrencies=self.__GetRandomIdList(conn,"Currency",count)

         priceList=np.random.randint(low = 0, high = 200000,size=count)  

         dict = {
                'Customer_Id':randomCustomers,
                'Company_Worker_Id':randomCompany_Workers,
                'Company_Services_Id':randomCompnay_Services,
                'state':stateList,
                'registrationDate' : registrationDateList,
                'doneDate': doneDateList,
                'isGraded' : isGraded,
                'currency_id': randomCurrencies,
                'price' : priceList}

         df = pd.DataFrame(dict)
         for rowIndex,row in df.iterrows():
             x=row.items()
             insertdata =  "("+str(row[0])+","+str(row[1])+","+str(row[2])+", "+str(row[3])+",  "+" Now() "+", "+" NOW() "+", "+str(row[6])+", "+str(row[7])+", "+str(row[8])+")"
             print("insertdata :",insertdata)
             cur=conn.cursor()

             cur.execute("insert into Orders(customer_id,company_worker_id,company_service_id,state,registerDate,doneDate,isGraded,currency_Id,price) values " + insertdata)

         cur.execute("insert into Orders(customer_id,company_worker_id,company_service_id,state,registerDate,doneDate,isGraded,currency_Id,price) values " + insertdata)

         conn.commit()
         conn.close()

   
    def __GetRandomIdList(self,conn,tableName,count):
        cur = conn.cursor()
        command = "select Id from " + tableName + ' ;' 
        df = psql.read_sql(command, conn)
        objList = df['id'].tolist()
        randomIndexes=np.random.randint(low = 0, high = len(objList)-1,size=count)

        randomObjList=[]
        for ind in randomIndexes:
            randomObjList.append(objList[ind])
        return randomObjList
         

