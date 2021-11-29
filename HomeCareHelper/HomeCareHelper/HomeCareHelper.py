import InitContext as ctx
import InitActions as act
import GenerateOrdersJob as g
str="host=localhost dbname=homecaretest user=postgres password=postgres"
#context= ctx.InitContext(str)
#actionsInit=act.InitActions(context)
#actionsInit.Init()

job=g.GenerateOrdersJob(2,str)
job.ExecuteJob()

