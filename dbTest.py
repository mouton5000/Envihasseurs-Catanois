from Jeu import *
from joueurs import *
from plateau import *
from cartes import *
from arbre_action import *
from user import *
import redis
import hashlib

REDIS = redis.StrictRedis()
REDIS.flushdb()
REDIS.set('lastBateauId',7)

User(1, 'test1', hashlib.sha1('test1').hexdigest()).save()
User(2, 'test2', hashlib.sha1('test2').hexdigest()).save()
User(3, 'test3', hashlib.sha1('test3').hexdigest()).save()
User(4, 'test4', hashlib.sha1('test4').hexdigest()).save()
User(5, 'test5', hashlib.sha1('test5').hexdigest()).save()
Joueur(1).setColor(255,0,0)
Joueur(2).setColor(0,0,255)
Joueur(3).setColor(0,255,0)
Joueur(4).setColor(100,100,100)
Joueur(5).setColor(200,200,50)

JoueurPossible.setNbJoueurs(5)

j = JoueurPossible(1)
p = Plateau.getPlateau()
tg = p.ter(1)
td = p.ter(2)

j.addTerre(tg)
j.addTerre(td)


Colonie(1,p.it(62)).save()
Colonie(2,p.it(64)).save()
c = Colonie(1,p.it(44))
c.evolue()
c.save()
Route(1,p.it(62).lien(p.it(72))).save()
Route(2,p.it(58).lien(p.it(59))).save()
Bateau(1,1,p.it(56).lien(p.it(57)),Cartes.RIEN,Bateau.BateauType.TRANSPORT,False).save()
Bateau(2,1,p.it(101).lien(p.it(102)),Cartes.RIEN,Bateau.BateauType.CARGO,False).save()
Bateau(3,1,p.it(7).lien(p.it(8)),Cartes.RIEN,Bateau.BateauType.VOILIER,False).save()
Bateau(4,2,p.it(90).lien(p.it(100)),Cartes.RIEN,Bateau.BateauType.CARGO,False).save()
Bateau(5,1,p.it(56).lien(p.it(57)),Cartes.RIEN,Bateau.BateauType.TRANSPORT,False).save()
Bateau(6,3,p.it(90).lien(p.it(100)),Cartes.RIEN,Bateau.BateauType.VOILIER,False).save()


cg = Tarifs.ROUTE*10 + Tarifs.COLONIE*10+ Tarifs.VILLE*10+Tarifs.BATEAU_TRANSPORT*10+Tarifs.CARGO*10+Tarifs.VOILIER*10
cd = Tarifs.ROUTE*2

j.recevoir(tg,cg)
j.addOr(tg,3)
j.set_route_la_plus_longue(tg,0)
j.setStaticPoints(tg,3)


j.recevoir(td,cd)
j.addOr(td,1)
j.set_route_la_plus_longue(td,0)
j.setStaticPoints(td,0)

j1 = Joueur(1)
n1 = j1.setNewRoot()
n2 = n1.addChild()
n3 = n2.addChild()
n4 = n1.addChild()
n5 = n2.addChild()
        
a1 = p.it(72).lien(p.it(82))
i1 = p.it(82)
a2 = p.it(82).lien(p.it(92))
a3 = p.it(62).lien(p.it(61))
a4 = p.it(61).lien(p.it(71))
act1 = Action(1, NodeCst.NULL, 'construire_route', a1.num)
act2 = Action(2, NodeCst.NULL, 'construire_route', a2.num)
act3 = Action(3, NodeCst.NULL, 'construire_colonie', i1.num)
act4 = Action(4, NodeCst.NULL, 'evoluer_colonie', i1.num)
#act5 = Action(5, NodeCst.NULL, 'evoluer_bateau', 7)
#act6 = Action(6, NodeCst.NULL, 'construire_route', a2.num)
#act7 = Action(7, NodeCst.NULL, 'construire_route', a2.num)
        
act1.save()
act2.save()
act3.save()
act4.save()
#act5.save()
#act6.save()
#act7.save()

n2.addAction(act1)
n3.addAction(act2)
n3.addAction(act3)
n3.addAction(act4)
#n3.addAction(act5)
#n4.addAction(act6)
#n5.addAction(act7)
        

Voleur(p.hexa(22),Voleur.VoleurType.BRIGAND,p.ter(1)).save(REDIS)
Voleur(p.hexa(1),Voleur.VoleurType.PIRATE,p.ter(1)).save(REDIS)

Voleur(p.hexa(25),Voleur.VoleurType.BRIGAND,p.ter(2)).save(REDIS)
Voleur(p.hexa(4),Voleur.VoleurType.PIRATE,p.ter(2)).save(REDIS)
