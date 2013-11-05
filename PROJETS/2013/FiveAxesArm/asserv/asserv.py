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
moteurs = ['base', 'epaule', 'coude', 'poignet', 'main']

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

"""
# remplie correctement le tableau etatMoteur[] avec :
# 1 si m est en train d'etre commandé par boutons, 0 sinon
void setEtatMoteurs(){
   for (byte m=0; m<5; m++) {
      # A FAIRE !!!
      etatMoteur[m] = 0;
   }
}
"""

def getCommandeBouton(m){
"""renvoie la commande associée aux boutons du moteur m"""
   # A FAIRE !!!
   return 0;
}

def potaToAngle(int valPota){
"""convertit la valeur valPota (0..1023) en un angle (-pi..pi)"""
   # A FAIRE !!!
   return 0.0;
}

###########################      FIN FONCTIONS      ##################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
##########################      INITIALISATION      ##################################

void setup() {

   for (byte m=0; m<5; m++) {

      # pin moteurs et sens moteurs en sortie :
      pinMode(pinPwmMoteur[m],OUTPUT);
      pinMode(pinSensMoteur[m],OUTPUT);

      # initialisation avec les positions initiales des moteurs
      potaMoteur[m] = analogRead(pinPotaMoteur[m]);
      angleMoteur[m] = potaToAngle(potaMoteur[m]);
      consigneAngleMoteur[m] = angleMoteur[m];
      etatMoteur[m] = 0;

   }

}

########################      FIN INITIALISATION      ################################
######################################################################################
######################################################################################

######################################################################################
######################################################################################
#############################      PROGRAMME      ####################################

void loop() {

   # déterminer l'état de chacun des moteurs (commandé par bouton ou asservi)
   setEtatMoteurs();

   # commander chacun des moteurs
   for (byte m=0; m<5; m++) {
      # si le moteur est asservi en angle
      if (etatMoteur[m] == 0) {
         ecart = getEcart(m);
         commande = getCommande(ecart);
         commanderMoteur(m,commande);
         # si le moteur est controllé par bouton
      } else {
         commande = getCommandeBouton(m);
         commanderMoteur(m,commande);
         potaMoteur[m] = analogRead(pinPotaMoteur[m]);
         angleMoteur[m] = potaToAngle(potaMoteur[m]);
         consigneAngleMoteur[m] = angleMoteur[m];
      }
   }
}

###########################      FIN PROGRAMME      ##################################
######################################################################################
######################################################################################

