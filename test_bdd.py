# *-* coding: iso-8859-1 *-*
import unittest
from bdd_interface import *
import redis

REDIS = redis.StrictRedis()

class TestBDD(unittest.TestCase):
    def setUp(self):
        # On crée un arbre avec une racine vide, sans fils. Le curseur est placé sur
        # la racine
        self.b1 = BDD()
        self.b2 = BDD(self.b1)
        REDIS.flushdb()

    def test_get_set(self):
        b1 = self.b1
        b2 = self.b2
        r = REDIS

        s1 = 'test1'
        v1 = 1
        sv1 = str(v1)

        s2 = 'test2'
        v2 = 2
        sv2 = str(v2)

        s3 = 'test3'
        v3 = 3
        sv3 = str(v3)

        self.assertEqual(r.get(s1), None)
        self.assertEqual(b1.get(s1), None)
        self.assertEqual(b2.get(s1), None)

        r.set(s1,v1)
        self.assertEqual(r.get(s1), sv1)
        self.assertEqual(b1.get(s1), sv1)
        self.assertEqual(b2.get(s1), sv1)
        
        b1.set(s2,v2)
        self.assertEqual(r.get(s2), None)
        self.assertEqual(b1.get(s2), sv2)
        self.assertEqual(b2.get(s2), sv2)
        
        b2.set(s3,v3)
        self.assertEqual(r.get(s3), None)
        self.assertEqual(b1.get(s3), None)
        self.assertEqual(b2.get(s3), sv3)

        b1.set(s1,v3)
        self.assertEqual(r.get(s1), sv1)
        self.assertEqual(b1.get(s1), sv3)
        self.assertEqual(b2.get(s1), sv3)
        
        b2.set(s1,v2)
        self.assertEqual(r.get(s1), sv1)
        self.assertEqual(b1.get(s1), sv3)
        self.assertEqual(b2.get(s1), sv2)

        b1.save() 
        self.assertEqual(r.get(s1), sv3)
        self.assertEqual(b1.get(s1), sv3)
        self.assertEqual(b2.get(s1), sv2)
        
        b2.save() 
        self.assertEqual(r.get(s1), sv3)
        self.assertEqual(b1.get(s1), sv2)
        self.assertEqual(b2.get(s1), sv2)
        
        b2.saveAll() 
        self.assertEqual(r.get(s1), sv2)
        self.assertEqual(b1.get(s1), sv2)
        self.assertEqual(b2.get(s1), sv2)

    def test_set(self):
        b1 = self.b1
        b2 = self.b2
        r = REDIS

        s1 = 'test1'
        v11 = 11
        v12 = 12
        v13 = 13
        v14 = 14
        sv11 = str(v11)
        sv12 = str(v12)
        sv13 = str(v13)
        
        self.assertEqual(r.smembers(s1), set([]))
        self.assertEqual(b1.smembers(s1), set([]))
        self.assertEqual(b2.smembers(s1), set([]))

        r.sadd(s1,v11)
        self.assertEqual(r.smembers(s1), set([sv11]))
        self.assertEqual(b1.smembers(s1), set([sv11]))
        self.assertEqual(b2.smembers(s1), set([sv11]))
        
        b1.sadd(s1,v12)
        self.assertEqual(r.smembers(s1), set([sv11]))
        self.assertEqual(b1.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b2.smembers(s1), set([sv11,sv12]))
        
        b2.sadd(s1,v13)
        self.assertEqual(r.smembers(s1), set([sv11]))
        self.assertEqual(b1.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b2.smembers(s1), set([sv11,sv12, sv13]))
        
        b2.srem(s1,v11)
        self.assertEqual(r.smembers(s1), set([sv11]))
        self.assertEqual(b1.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b2.smembers(s1), set([sv12, sv13]))

        self.assertTrue(b1.sismember(s1,sv12))
        self.assertFalse(r.sismember(s1,sv12))
        self.assertFalse(b2.sismember(s1,sv11))
        
        b1.save()
        self.assertEqual(r.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b1.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b2.smembers(s1), set([sv12, sv13]))
        
        b2.save()
        self.assertEqual(r.smembers(s1), set([sv11,sv12]))
        self.assertEqual(b1.smembers(s1), set([sv12, sv13]))
        self.assertEqual(b2.smembers(s1), set([sv12, sv13]))
        
        b2.saveAll()
        self.assertEqual(r.smembers(s1), set([sv12,sv13]))
        self.assertEqual(b1.smembers(s1), set([sv12, sv13]))
        self.assertEqual(b2.smembers(s1), set([sv12, sv13]))
    
    def test_list(self):
        b1 = self.b1
        b2 = self.b2
        r = REDIS

        s1 = 'test1'
        v11 = 11
        v12 = 12
        v13 = 13
        v14 = 14
        v15 = 15
        sv11 = str(v11)
        sv12 = str(v12)
        sv13 = str(v13)
        sv14 = str(v14)
        sv15 = str(v15)
        
        self.assertEqual(r.lrange(s1,0,-1), [])
        self.assertEqual(b1.lrange(s1,0,-1), [])
        self.assertEqual(b2.lrange(s1,0,-1), [])

        r.lpush(s1,v11) 
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv11])
        
        b1.lpush(s1,v12) 
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv11])

        b2.rpush(s1,v13) 
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv11,sv13])
        self.assertEqual(r.llen(s1), 1)
        self.assertEqual(b1.llen(s1), 2)
        self.assertEqual(b2.llen(s1), 3)
        self.assertEqual(r.lindex(s1,0), sv11)
        self.assertEqual(b1.lindex(s1,1), sv11)
        self.assertEqual(b2.lindex(s1,2), sv13)

        b2.linsert(s1,'before',v11,v14)
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv11,sv13])
        
        b2.linsert(s1,'after',v11,v15)
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv11,sv15,sv13])

        b2.rpush(s1,v11) 
        b2.lpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.lrem(s1,0,v11)
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv15,sv13])
        
        b2.rpush(s1,v11) 
        b2.lpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.lrem(s1,-2,v11)
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv11,sv12,sv14,sv15,sv13,sv11])
        
        b2.rpush(s1,v11) 
        b2.lpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.rpush(s1,v11) 
        b2.lrem(s1,3,v11)
        self.assertEqual(r.lrange(s1,0,-1), [sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])

        b1.save()
        self.assertEqual(r.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])
        
        b2.save()
        self.assertEqual(r.lrange(s1,0,-1), [sv12,sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])
        

        b2.saveAll()
        self.assertEqual(r.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])
        self.assertEqual(b1.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])
        self.assertEqual(b2.lrange(s1,0,-1), [sv12,sv14,sv15,sv13,sv11,sv11,sv11])

if __name__ == '__main__':
    unittest.main()
