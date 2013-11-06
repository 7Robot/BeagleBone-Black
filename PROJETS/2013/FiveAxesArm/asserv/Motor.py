from math import *

class Motor :
   """Classe définissant un moteur, caractérisé par :
   - le rapport de cycle de son PWM
   - la pin de son PWM
   - son sens de rotation
   - la pin de son sens de rotation
   - la valeur de son potentiomètre
   - la pin de son potentiomètre
   - son angle actuel
   - sa consigne angulaire
   - son état (commandé par bouton ou asservi)"""

   def __init__(self, nom, pinPwm, pinSens, pinPota, angleMin=-pi, angleMax=pi, potaMin=0.0, potaMax=1.0, consigneAngle=0.0, etat=0) :
      """Initialisation de l'instance de Motor"""

      self.nom = nom
      self.pwm = 0
      self.pinPwm = pinPwm
      self.sens = 0
      self.pinSens = pinSens
      self.pota = 0.0
      self.pinPota = pinPota
      self.angle = 0.0
      self.consigneAngle = consigneAngle
      self.etat = etat

      # min et max des valeur du pota et correspondance en angle
      self.angleMin = angleMin
      self.angleMax = angleMax
      self.potaMin = potaMin
      self.potaMax = potaMax

   def getEcart(self) :
      """Renvoie l'écart entre la consigne angulaire et l'angle actuel"""
      return self.consigneAngle - self.angle

   def getCommande(self) :
      """Renvoie une commande pour le moteur"""
      # A FAIRE
      return 0

   def commander(self, commande) :
      """Commander ce moteur avec une commande"""
      # A FAIRE

   def potaToAngle() :
      """Transforme la valeur du pota en un angle en fonction des caractéristiques du pota"""
      # A FAIRE
      return 0.0
