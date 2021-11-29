from abc import ABCMeta , abstractmethod

class Job(object):
    
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def RepeatInterval(self):
        pass

    @property
    @abstractmethod
    def ConnStr(self):
        pass

    @abstractmethod
    def ExecuteJob(self):
        pass

  

