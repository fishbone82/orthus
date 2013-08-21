import json
from sqlalchemy import text, ForeignKey, Column, Integer, TIMESTAMP, Enum, String
from workers import Worker as WorkerClass
from __init__ import Session, Mongo, ORMBase
from hosts import Host as HostClass
mongo = Mongo


class Check(ORMBase):
    __tablename__ = 'checks'
    check_id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.host_id'))
    state = Column(Enum('-1', '0', '1', '2'))
    check_interval = Column(Integer)
    next_check = Column(TIMESTAMP)
    plugin = Column(String)
    args = Column(String)
    workers = Column(String)

    def generate_token(self):
        return "G654hpx5"

    def get_workers(self):
        session = Session()
        workers_list = json.loads(self.workers)
        workers = session.query(WorkerClass).filter(WorkerClass.worker_id.in_(workers_list)).all()
        session.close()
        return workers

    def args_dict(self):
        args_dict = json.loads(self.args)
        args_dict['token'] = self.generate_token()
        return args_dict

    def get_mongo_collection(self):
        collection = getattr(mongo, 'user_%s' % self.host.user_id)
        return collection

    def update_results(self, results):
        print results
        # update next_check time in MySQL
        session = Session()
        self.next_check = text('NOW() + INTERVAL check_interval SECOND')
        self.state = '0'  # -1 = active but never checked, 0 = active and checked 1 = disabled
        session.merge(self)
        #print "QQQ: %s" % self.host
        session.flush()
        session.close()

        # push results to mongo
        #collection = self.get_mongo_collection()
        #collection.insert({"check_id": check.check_id, "results": check_results})



    # def __init__(self, host_id, state,  plugin,  next_check=None, check_interval=600):
    #     self.host_id = host_id
    #     self.plugin = plugin
    #     self.state = state
    #     self.check_interval = check_interval
    #     self.next_check = next_check
