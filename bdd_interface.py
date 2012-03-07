import redis

REDIS = redis.StrictRedis()

class BDD:

    def __init__(self):
        self.dict = {}

    def set(self,key,value):
        self.dict[key] = str(value)

    def get(self,key):
        return self.dict[key]

    def exists(self,key):
        return key in self.dict

    def keys(self):
        return self.dict.keys()

    def sadd(self,key,value):
        if not self.exists(key):
            self.dict[key] = set([])
        self.dict[key].add(str(value))

    def srem(self,key,value):
        if (self.exists(key)):
            self.dict[key].remove(str(value))

    def flushdb(self):
        self.dist.clear()

    def save(self):
        pipe = REDIS.pipeline()
        for key in self.keys():
            v = self.dict[key]
            if isinstance(v,set):
                for i in v:
                    pipe.sadd(key,i)
            else:
                pipe.set(key,v)
        pipe.execute()
