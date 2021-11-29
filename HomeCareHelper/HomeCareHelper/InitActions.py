import InitContext
import psycopg2
import pandas.io.sql as psql
import pandas as pd
import numpy as np
from pathlib import Path
import schedule



class InitActions(object):
    Context=None

    # parameterized constructor
    def __init__(self, context):
        self.Context=context
    
    def  __ExecuteSQLScript(self,cur):
         path = Path(self.Context.dp_create_script_path)
         with open(path, 'r') as f:
            command = f.read()
            cur.execute(command)

    def __LoadDataFromCSV(self,filepath,tablename,cur):
        path = Path(filepath)
        with open(path, 'r') as f:
            next(f)
            cur.copy_from(f, tablename, sep=',') 

    def __LoadData(self,cur): 
        for key in self.Context.table_csv_dictionary.keys():
            filepath = self.Context.folderPath +  self.Context.table_csv_dictionary[key]
            tablename = key
            self.__LoadDataFromCSV(filepath,tablename,cur)

    def __LoadSpecificTablesData(self,cur):        
        #region LoadWorkers
        path = " 'C://Users//Maga//Downloads//Workers.csv '"
        command = "COPY Worker(Id,name,phonenumber) FROM " + path + " DELIMITER ','  CSV HEADER;"
        cur.execute(command)
        #endregion
        #region LoadCompany_Workers
        path = " 'C://Users//Maga//Downloads//Company_Workers.csv '"
        command = "create table temp(id int, worker_id int, company_id int); " + " COPY temp(worker_id,company_id) FROM  " + path + " DELIMITER ','  CSV HEADER; " + " insert into Company_Worker(Worker_Id,Company_Id) SELECT Worker_Id,Company_Id FROM temp GROUP BY Worker_Id,Company_Id HAVING COUNT(*) = 1; drop table temp;"
        cur.execute(command)
        #endregion
        #region LoadCompany_Services
        path = " 'C://Users//Maga//Downloads//Company_Service.csv '"
        command = "create table temp (company_id int, service_id int); " + " COPY temp(company_id,service_id) FROM  " + path + " DELIMITER ','  CSV HEADER; " + " insert into Company_Service(Company_Id,Service_Id) SELECT Company_Id,Service_Id FROM temp GROUP BY Company_Id, Service_id  HAVING COUNT(*) = 1; drop table temp"
        cur.execute(command)
        #endregion

    def __Generate_Company_Workers_Company_Service(self,conn):
        command = "select Id from Company_Worker;"
        df = psql.read_sql(command, conn)
        Company_Workers_Id_List = df['id'].tolist()
        randomWorkersIndexes = np.random.randint(low = 0, high = len(Company_Workers_Id_List)-1, size = 250)
        randomWorkers=[]
        for ind in randomWorkersIndexes:
            randomWorkers.append(Company_Workers_Id_List[ind])
        print(randomWorkers)

        command = "select Id from Company_Service;"
        df = psql.read_sql(command, conn)
        Company_Services_Id_List = df['id'].tolist()
        randomServicesIndexes = np.random.randint(low = 0, high = len(Company_Services_Id_List)-1, size = 250)
        randomServices=[]
        for ind in randomServicesIndexes:
            randomServices.append(Company_Services_Id_List[ind])
        print(randomServices)

        benefitPercentList = np.random.randint(low=10,high=100,size=250)
        print(benefitPercentList)

        dict = {'Company_Worker_Id':randomWorkers,'Company_Services_Id':randomServices, 'benefit_percent':benefitPercentList}
        df = pd.DataFrame(dict)
        print(df)
        benefit_percent__maxes = df.groupby(['Company_Worker_Id', 'Company_Services_Id']).benefit_percent.transform(max)
        df = df.loc[df.benefit_percent == benefit_percent__maxes]
        print(df)  

        for rowIndex,row in df.iterrows():
             x=row.items()
             insertdata =  "("+str(row[0])+","+str(row[1])+","+str(row[2])+")"
             print("insertdata :",insertdata)
             cur=conn.cursor()
             cur.execute("insert into Company_Worker_Company_Service(company_worker_id,company_service_id,benefit_percent) values " + insertdata)
             print( "row inserted:", insertdata)

    def __StartJobs(self):
        i=0;
        while i < len(self.Context.Jobs):
            schedule.every(self.Context.Jobs[i].RepeatInterval).minutes.do(self.Context.Jobs[i].ExecuteJob)
            i=i+1
        while  True :
            schedule.run_pending()
            

    
    def Init(self):
        #conn = psycopg2.connect(self.Context.db_connection_string)
        #cur = conn.cursor()
        #self.__ExecuteSQLScript(cur)
        #self.__LoadData(cur)
        #self.__LoadSpecificTablesData(cur)
        #self.__Generate_Company_Workers_Company_Service(conn)
        #conn.commit()
        #conn.close()
        self.__StartJobs()



        
