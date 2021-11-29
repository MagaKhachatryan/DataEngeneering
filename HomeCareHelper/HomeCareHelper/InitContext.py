import GenerateOrdersJob as g

class InitContext(object):
    db_connection_string = ""
    dp_create_script_path = ""
    table_csv_dictionary = "" 
    folderPath=""
    Jobs=[]
    
    # parameterized constructor
    def __init__(self, str):
        self.db_connection_string=str
        self.dp_create_script_path='C:\\Users\Maga\\Downloads\\HomeCareDBScript'
        self.folderPath="C:\\Users\Maga\\Downloads\\"
        self.table_csv_dictionary={'currency':'Currencies.csv',
                              'country':'Countries.csv',
                              'city': 'Cities.csv',
                              'street':'Street.csv',
                              'address':'Addresses.csv',
                              'customer':'Customers.csv',
                              'category':'Categories.csv',
                              'service':'Services.csv',
                              'company':'Companies.csv'}
        job=g.GenerateOrdersJob(1,self.db_connection_string)
        self.Jobs.append(job)

        





