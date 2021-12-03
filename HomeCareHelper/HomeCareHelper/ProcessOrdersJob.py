import psycopg2
from pathlib import Path

class ProcessOrdersJob(object):
    RepeatInterval=None
    ConnStr=None

    def __init__(self,interval,connstr):
        self.RepeatInterval = interval
        self.ConnStr=connstr

    def ExecuteJob(self):
         conn = psycopg2.connect(self.ConnStr)
         cur=conn.cursor()
         path = Path('C:\\Users\Maga\\Desktop\\DataEngeneering\\HomeCareHelper\\ProcessOrdersJobScript')
         with open(path, 'r') as f:
            command = f.read()
            cur.execute(command)
         conn.commit()
         conn.close()


