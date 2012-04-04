import unittest

import redis
import Jeu
from joueurs import *
from pions import *
from plateau import *
from errors import *
from cartes import *
from ActionNight import *

REDIS = redis.StrictRedis()

class TestJoueur(unittest.TestCase):

    def setUp(self):
        REDIS.flushdb()
        self.p = Plateau.getPlateau()
        self.p.reinit()
    
        mer = HexaType.MER
        arg = HexaType.ARGILE
        bois = HexaType.BOIS
        cai = HexaType.CAILLOU
        ble = HexaType.BLE
        mou = HexaType.MOUTON
        aur = HexaType.OR
        des = HexaType.DESERT
    
        ctou = CommerceType.TOUS
        cboi = CommerceType.BOIS
        carg = CommerceType.ARGILE
        ccai = CommerceType.CAILLOU
        cble = CommerceType.BLE
        cmou = CommerceType.MOUTON

        self.p.build(12,10,[(mer, 0,0,0),(mer, 0,ctou,3),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(ble, 3,0,0),(mer, 0,0,0),(mer, 0,0,0),(bois, 12,0,0),(bois, 9,0,0),(cai, 8,0,0),(mer, 0,0,0),(ble, 9,0,0),(mer, 0,0,0),(mer, 0,0,0),(des, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(aur, 4,0,0),(aur, 6,0,0),(ble, 10,0,0),(mer, 0,0,0),(des, 0,ctou,0),(mer, 0,0,0),(mer, 0,0,0),(des, 0,ctou,0),(mer, 0,0,0),(mer, 0,0,0),(mou, 8,0,0),(des, 0,carg,0),(mou, 5,0,0),(mer, 0,0,0),(arg, 6,0,0),(mer, 0,0,0),(mer, 0,0,0),(arg, 5,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,cble,0),(mer, 0,0,0),(bois, 9,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,cmou,0),(mer, 0,0,0),(mer, 0,0,0),(mer, 0,0,0)],[('Terre Gauche',[12,16,17,22,26,27,32,36,37,42,47],[1,2,3,6,7,8,11,13,18,21,23,28,31,33,38,41,43,46,48,51,52,53,56,57,58]),('Terre Droite',[15,19,25,29,35,39,45],[4,5,9,10,14,20,24,30,34,40,44,45,49,50,54,55,59,60])])

        Voleur(self.p.hexa(22),Voleur.VoleurType.BRIGAND,self.p.ter(1)).save(REDIS)
        Voleur(self.p.hexa(1),Voleur.VoleurType.PIRATE,self.p.ter(1)).save(REDIS)
        
        Voleur(self.p.hexa(25),Voleur.VoleurType.BRIGAND,self.p.ter(2)).save(REDIS)
        Voleur(self.p.hexa(4),Voleur.VoleurType.PIRATE,self.p.ter(2)).save(REDIS)


if __name__ == '__main__':
   unittest.main()
