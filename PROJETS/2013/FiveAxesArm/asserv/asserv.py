# -*-coding:Utf-8 -*

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
from Motor import *
import time
from math import *

######################################################################################
# L'objectif de ce programme est d'asservir en angles chacun des 5 moteurs du bras   #
######################################################################################
"""
L'algorithme se base sur le principe suivant :
Chaque moteur peut avoir 2 états différents :
   1) commandé par appui sur bouton
   2) asservi en angle

Voila  le principe de l'algorithme : 
"""
######################################################################################
######################################################################################
#############################      ALGORITHME     ####################################
"""
Pour chaque moteur :
   si le moteur est asservi en angle
      ecart = getEcart(moteur)
      commande = getCommande(ecart)
      commanderMoteur(moteur, commande)
   sinon (moteur commandé par bouton)
      commande = getCommandeBouton(moteur)
      commanderMoteur(moteur, commande)
      maj les valeurs de consignes angulaire avec la position actuelle
"""
#############################    FIN ALGORITHME     ##################################
######################################################################################
######################################################################################
"""
où commande est un entier dans [[-255 ; 255]]
et commanderMoteur(moteur,commande) effectue les différentes actions suivantes :
renvoi un PWM proportionnel a |commande|
active ou non la pin de sens suivant le signe de commande
"""
######################################################################################
######################################################################################
#############################      VARIABLES      ####################################

# les moteurs
nomMoteurs = ['base', 'epaule', 'coude', 'poignet', 'main']
moteurs = []

# pin d'activation des moteurs
pinEnableMoteur = ["P9_11","P9_12","P9_23","P9_24","P9_26"]

# pin des moteurs
pinPwmMoteur = ["P9_14","P9_16","P9_22","P8_13","P8_19"]

# sens des moteurs
pinSensMoteur = ["P9_13","P9_15","P9_21","P8_14","P8_20"]

# pota des moteurs
pinPotaMoteur = ["P9_35","P9_36","P9_33","P9_38","P9_39"]

# bouton de demarrage
pinBouton = "P8_10"

# pin test
#pinTest = ["P9_11","P9_12","P9_17","P9_18","P9_19","P9_20","P9_23","P9_24","P9_25","P9_26","P9_27","P9_28","P9_41","P9_42"]

# angleMin angleMax potaMin et potaMax
angleMinMoteur = [-pi,0.0,0,-pi,-pi/2]
angleMaxMoteur = [+pi,+pi/2,+pi/2,+pi,+pi/2]
potaMinMoteur = [0.223, 0.216, 0.485, 0.701, 0.321]
potaMaxMoteur = [0.777, 0.356, 0.354, 0.302, 0.693]

# etats des moteurs (0 = asservi et 1 = commandé)
etatMoteur = [0,0,0,0,0]

# autres variables
commande = 0 # entier entre -255 et +255 représentant la commande à envoyer au moteur


###########################      FIN VARIABLES      ##################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
#############################      FONCTIONS      ####################################

def setEtatMoteurs(moteurs) :
   """met correctement a jour les états des moteurs :
   1 si m est en train d'etre commandé par boutons, 0 sinon"""
   for m in moteurs :
      # A FAIRE !!!
      m.etat = 0

def getCommandeBouton(m) :
   """renvoie la commande associée aux boutons du moteur m"""
   # A FAIRE !!!
   return 0

def majConsignesAngles(moteurs, consignesAngles) :
   """ met a jour les consignes angulaires des moteurs avec le tableau consignesAngles"""
   for i,m in enumerate(moteurs) :
      m.consigneAngle = consignesAngles[i]


###########################      FIN FONCTIONS      ##################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
##########################      INITIALISATION      ##################################

# activation des entrées analogiques
ADC.setup()

# declaration du bouton
GPIO.setup(pinBouton,GPIO.IN)

# declaration des pins de test
#for pin in pinTest :
#   GPIO.setup(pin,GPIO.OUT)

for i,nom in enumerate(nomMoteurs) :

   # création des objets Moteur
   m = Motor(nom,pinEnableMoteur[i],pinPwmMoteur[i],pinSensMoteur[i],pinPotaMoteur[i],angleMinMoteur[i],angleMaxMoteur[i],potaMinMoteur[i],potaMaxMoteur[i])
   moteurs.append(m)

for m in moteurs :

   # pin d'activation des moteurs en sortie :
   GPIO.setup(m.pinEnable,GPIO.OUT)
   print(m.nom + " enable : " + m.pinEnable)

   # pin sens moteurs en sortie :
   GPIO.setup(m.pinSens,GPIO.OUT)

   # initialisation avec les positions initiales des moteurs
   m.majPota()
   m.majAngle()
   m.consigneAngle = m.angle
   m.etat = 0

for m in moteurs :
   GPIO.output(m.pinEnable,GPIO.LOW)
   GPIO.output(m.pinSens,GPIO.LOW)
   commande = 0.0
   PWM.start(m.pinPwm, commande)

########################      FIN INITIALISATION      ################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
#############################      PROGRAMME      ####################################

# TEST : donner des consignes angulaires initiales
# consignesAngles = [0.3, 0.3, 0.3, 0.0, 0.0]
# majConsignesAngles(moteurs, consignesAngles)
moteurs[0].consigneAngle = 0.0
moteurs[1].consigneAngle = pi/4
moteurs[2].consigneAngle = pi/3
"""moteurs[1].consigneAngle = 0.3
moteurs[2].consigneAngle = 0.3
moteurs[3].consigneAngle = 0.3
moteurs[4].consigneAngle = 0.3

while True :
   moteurs[0].commander(100)"""

while (GPIO.input(pinBouton) == 0) :
   time.sleep(0.01)

   """for pin in pinTest :
      GPIO.output(pin,GPIO.HIGH)
   time.sleep(2)
   for pin in pinTest :
      GPIO.output(pin,GPIO.LOW)
   time.sleep(2)
   #print("not ready")"""

# activation de la base
#GPIO.output(moteurs[0].pinEnable,GPIO.HIGH)
GPIO.output(moteurs[1].pinEnable,GPIO.HIGH)
GPIO.output(moteurs[2].pinEnable,GPIO.HIGH)
print("ready")
# FIN TEST

while True :

   # déterminer l'état de chacun des moteurs (commandé par bouton ou asservi)
   setEtatMoteurs(moteurs)

   # commander chacun des moteurs
   for m in moteurs :
      # si le moteur est asservi en angle
      if m.etat == 0 :
         m.majPota()
         m.majAngle()
         commande = m.getCommande()
         if m.nom == "main" :
            print("pota :" + str(m.pota) + "   angle : "+ str(m.angle) + "   commande : "+ str(commande))
         #m.commander(commande)
      # si le moteur est controllé par bouton
      else :
         commande = getCommandeBouton(m)
         m.commander(commande)
         m.majPota()
         m.majAngle()
         m.consigneAngle = m.angle

   # temps (en s) a attendre pour laisser un peu les PWM faire leur effet
   time.sleep(0.001)

# arret des PWM, ADC et GPIO

###########################      FIN PROGRAMME      ##################################
######################################################################################
######################################################################################
