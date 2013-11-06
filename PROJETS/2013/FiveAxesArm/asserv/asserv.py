import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
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

Voilà le principe de l'algorithme : 
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
renvoi un PWM proportionnel à |commande|
active ou non la pin de sens suivant le signe de commande
"""
######################################################################################
######################################################################################
#############################      VARIABLES      ####################################

# les moteurs
nomMoteurs = ['base', 'epaule', 'coude', 'poignet', 'main']
moteurs = []

# pin des moteurs
pinPwmMoteur = ["P9.14","P9.16","P9.22","P8.13","P8.19"]

# sens des moteurs
pinSensMoteur = ["P9.13","P9.15","P9.21","P8.14","P8.20"]

# pota des moteurs
pinPotaMoteur = ["P9.35","P9.36","P9.37","P9.38","P9.39"]

# angleMin angleMax potaMin et potaMax
angleMinMoteur = [-pi,-pi,-pi,-pi,-pi]
angleMaxMoteur = [+pi,+pi,+pi,+pi,+pi]
potaMinMoteur = [0.0, 0.0, 0.0, 0.0, 0.0]
potaMaxMoteur = [1.0, 1.0, 1.0, 1.0, 1.0]

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
   """met correctement à jour les états des moteurs :
   1 si m est en train d'etre commandé par boutons, 0 sinon"""
   for m in moteurs :
      # A FAIRE !!!
      m.etat = 0

def getCommandeBouton(m) :
   """renvoie la commande associée aux boutons du moteur m"""
   # A FAIRE !!!
   return 0

def majConsignesAngles(moteurs, consignesAngles) :
   """ met à jour les consignes angulaires des moteurs avec le tableau consignesAngles"""
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

for i,nom in enumerate(nomMoteurs) :

   # création des objets Moteur
   m = Motor(nom,pinPwmMoteur[i],pinSensMoteur[i],pinPotaMoteur[i],angleMinMoteur[i],angleMaxMoteur[i],potaMinMoteur[i],potaMaxMoteur[i])
   moteurs.append(m)

   # pin sens moteurs en sortie :
   GPIO.setup(m.pinSens,GPIO.OUT)

   # initialisation avec les positions initiales des moteurs
   m.pota = ADC.read(m.pinPota)
   m.angle = m.potaToAngle()
   m.consigneAngle = m.angle
   m.etat = 0

########################      FIN INITIALISATION      ################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
#############################      PROGRAMME      ####################################

# TEST : donner des consignes angulaires initiales
consignesAngles = [0.3, 0.3, 0.3, 0.0, 0.0]
majConsignesAngles(moteurs, consignesAngles)
# FIN TEST

while True :

   # déterminer l'état de chacun des moteurs (commandé par bouton ou asservi)
   setEtatMoteurs(moteurs)

   # commander chacun des moteurs
   for m in moteurs :
      # si le moteur est asservi en angle
      if m.etat == 0 :
         commande = m.getCommande()
         m.commander(commande)
         # si le moteur est controllé par bouton
      else :
         commande = getCommandeBouton(m)
         m.commander(commande)
         m.majPota()
         m.majAngle()
         m.consigneAngle = m.angle

###########################      FIN PROGRAMME      ##################################
######################################################################################
######################################################################################
