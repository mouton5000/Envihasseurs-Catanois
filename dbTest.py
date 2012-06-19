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

Colonie(1,p.it(63)).save()
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


cg = Tarifs.ROUTE*4 + Tarifs.COLONIE*2
cd = Tarifs.ROUTE*2

j.recevoir(tg,cg)
j.addOr(tg,3)
j.set_route_la_plus_longue(tg,0)

j.recevoir(td,cd)
j.addOr(td,1)
j.set_route_la_plus_longue(td,0)

j1 = Joueur(1)
n1 = j1.setNewRoot()
n2 = n1.addChild()
n3 = n2.addChild()
n4 = n1.addChild()
n5 = n2.addChild()
        
a1 = p.it(62).lien(p.it(52))
a2 = p.it(52).lien(p.it(53))
act1 = Action(1, 'construire_route', a1.num)
act2 = Action(2, 'construire_route', a2.num)
act3 = Action(3, 'construire_route', a1.num)
act4 = Action(4, 'construire_route', a2.num)
act5 = Action(5, 'construire_route', a2.num)
        
act1.save()
act2.save()
act3.save()
act4.save()
act5.save()

n2.addAction(act1)
n3.addAction(act2)
n4.addAction(act3)
n4.addAction(act4)
n5.addAction(act5)
        

Voleur(p.hexa(22),Voleur.VoleurType.BRIGAND,p.ter(1)).save(REDIS)
Voleur(p.hexa(1),Voleur.VoleurType.PIRATE,p.ter(1)).save(REDIS)

Voleur(p.hexa(25),Voleur.VoleurType.BRIGAND,p.ter(2)).save(REDIS)
Voleur(p.hexa(4),Voleur.VoleurType.PIRATE,p.ter(2)).save(REDIS)
