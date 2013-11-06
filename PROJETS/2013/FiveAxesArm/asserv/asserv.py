import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
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
pinPwmMoteur = [3,5,6,9,10]

# sens des moteurs
pinSensMoteur = [2,4,7,8,12]

# pota des moteurs
pinPotaMoteur = [A0,A1,A2,A3,A4]

# consigne angulaire des moteurs
consigneAngleMoteur = [0.0, 0.0, 0.0, 0.0, 0.0]

# etats des moteurs (0 = asservi et 1 = commandé)
etatMoteur = [0,0,0,0,0]

# communication serie
baudRate = 9600 # en bits/s

# autres variables
ecart = 0.0 # ecart angulaire entre la consigne et l'angle actuel
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
   m = Motor(nom,pinPwmMoteur[i],pinSensMoteur[i],pinPotaMoteur[i])
   moteurs.append(m)

   # pin moteurs et sens moteurs en sortie :
   GPIO.setup(m.pinPwm,OUT);
   GPIO.setup(m.pinSens,OUT);

   # initialisation avec les positions initiales des moteurs
   m.pota = ADC.read(m.pinPota)
   m.angle = m.potaToAngle();
   m.consigneAngle = m.angle;
   m.etat = 0;

########################      FIN INITIALISATION      ################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
#############################      PROGRAMME      ####################################

while True :

   # déterminer l'état de chacun des moteurs (commandé par bouton ou asservi)
   setEtatMoteurs(moteurs)

   # commander chacun des moteurs
   for m in moteurs :
      # si le moteur est asservi en angle
      if m.etat == 0 :
         ecart = m.getEcart()
         commande = m.getCommande()
         m.commander(commande)
         # si le moteur est controllé par bouton
      else :
         commande = getCommandeBouton(m)
         m.commander(commande)
         m.pota = ADC.read(m.pinPota)
         m.angle = m.potaToAngle();
         m.consigneAngle = m.angle;
      }
   }
}

###########################      FIN PROGRAMME      ##################################
######################################################################################
######################################################################################
