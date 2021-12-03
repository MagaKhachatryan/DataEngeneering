import InitContext as ctx
import InitActions as act
import GenerateOrdersJob as g
import ProcessOrdersJob as p
import GenerateCanceledOrdersJob as pc

str="host=localhost dbname=homecaretest user=postgres password=postgres"
#context= ctx.InitContext(str)
#actionsInit=act.InitActions(context)
#actionsInit.Init()
#job=g.GenerateOrdersJob(1,str)
#job.ExecuteJob()
#job=p.ProcessOrdersJob(1,str)
#job.ExecuteJob()
job=pc.GenerateCanceledOrdersJob(1,str)
job.ExecuteJob()