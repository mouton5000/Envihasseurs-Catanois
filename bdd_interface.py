# *-* coding: iso-8859-1 *-*
import redis
import copy

REDIS = redis.StrictRedis()
class BDD:

    DELETE_TYPE = {'set' : set([]), 'list' : []}

    def __init__(self, bdd = REDIS):
        self.dict = {}
        self.bdd = bdd

    def type(self,key):
        if key in self.dict:
            return str(type(self.dict[key]))
        else:
            return self.bdd.type(key)
        
    
    def set(self,key,value):
        self.dict[key] = str(value)

    def get(self,key):
        if key in self.dict:
            return self.dict[key]
        else:
            return self.bdd.get(key)

    def exists(self,key):
        if key in self.dict:
            return True
        else:
            return self.bdd.exists(key)

    def keys(self):
        keys = self.bdd.keys()
        return list(set(self.dict.keys() + keys))

    def sismember(self,key,member):
        if key in self.dict:
            return str(member) in self.dict[key]
        else:
            return self.bdd.ismember(key,member)

    def smembers(self,key):
        if key in self.dict:
            return self.dict[key]
        else:
            return self.bdd.smembers(key)

    def sadd(self,key,value):
        if not key in self.dict or self.dict[key] == None:
            self.dict[key] = copy.copy(self.smembers(key))
        self.dict[key].add(str(value))

    def srem(self,key,value):
        if not key in self.dict or self.dict[key] == None:
            self.dict[key] = copy.copy(self.smembers(key))
        self.dict[key].remove(str(value))

    def linsert(self,key,after,pivot,value):
        if not key in self.dict:
            self.dict[key] = self.bdd.lrange(key,0,-1)
        a = self.dict[key]
        i = a.index(str(pivot))
        bafter = (after == 'after')
        if bafter:
            i += 1
        # Si c'est after, on insère sur l'indice suivant, sinon sur l'indice précédent.
        a.insert(i,str(value))

    def llen(self, key):
        if key in self.dict:
            return len(self.dict[key])
        return self.bdd.llen(key)
        

    def lindex(self, key, index):
        if key in self.dict:
            return self.dict[key][index]
        return self.bdd.lindex(key, index)

    def lpush(self, key, value):
        if not key in self.dict:
            self.dict[key] = self.bdd.lrange(key,0,-1)
        self.dict[key].insert(0,str(value))

    def lrange(self,key,i1,i2):
        if key in self.dict:
            a = self.dict[key]
            return a[i1:i2] + [a[i2]]
        else:
            return self.bdd.lrange(key,i1,i2)
        
    def lrem(self,key,count, value):
        if not key in self.dict:
            self.dict[key] = self.bdd.lrange(key,0,-1)
        a = self.dict[key]
        svalue = str(value)
        if count == 0:
            while svalue in a:
                a.remove(svalue)
        else:
            if count < 0:
                a.reverse()
            for i in xrange(0,abs(count)):
                a.remove(svalue)
            if count < 0:
                a.reverse()

    def rpush(self,key,value):
        if not key in self.dict:
            self.dict[key] = self.bdd.lrange(key,0,-1)
        self.dict[key].append(str(value))

    def flushdb(self):
        ''' Supprime les clés de la base de donnée entière '''
        self.bdd.flushdb()
        self.flushSurface()
    
    def flushSurface(self):
        ''' Ne supprime que les clés de la base de donné virtuelle '''
        self.dict.clear()

    def delete(self, key):
        ''' Supprime cette clé de la base de donnée vitruelle, pour éviter des problèmes, cette clé est virtuellement supprimée : sa valeur est mise à None. On saura ainsi faire la différence entre une clé supprimée et une clé qui n'est pas utilisée dans la base virtuelle. '''
        t = self.type(key)
        if t in BDD.DELETE_TYPE.keys():
            self.dict[key] = BDD.DELETE_TYPE[self.type(key)]
        else:
            self.dict[key] = None

    def save(self):
        for key in self.dict.keys():
            v = self.dict[key]
            if isinstance(v,set):
                self.bdd.delete(key)
                for i in v:
                    self.bdd.sadd(key,i)
            elif isinstance(v,list):
                self.bdd.delete(key)
                for i in v:
                    self.bdd.rpush(key,i)
            else:
                self.bdd.set(key,v)
        self.flushSurface()


    def saveAll(self):
        self.save()
        if self.bdd != REDIS:
            self.bdd.saveAll()
