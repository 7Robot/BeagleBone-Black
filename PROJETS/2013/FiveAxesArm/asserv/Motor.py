# -*-coding:Utf-8 -*

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time
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

   def __init__(self, nom, pinEnable, pinPwm, pinSens, pinPota, angleMin=-pi, angleMax=pi, potaMin=0.0, potaMax=1.0, consigneAngle=0.0, etat=0) :
      """Initialisation de l'instance de Motor"""

      self.nom = nom
      self.pinEnable = pinEnable
      self.pwm = 0
      self.pinPwm = pinPwm
      self.sens = 0
      self.pinSens = pinSens
      self.pota = 0.0
      self.pinPota = pinPota
      self.angle = 0.0
      self.consigneAngle = consigneAngle
      self.etat = etat
      self.sommeErreur = 0.0

      # min et max des valeur du pota et correspondance en angle
      self.angleMin = angleMin
      self.angleMax = angleMax
      self.potaMin = potaMin
      self.potaMax = potaMax

   def getEcart(self) :
      """Renvoie l'écart entre la consigne angulaire et l'angle actuel"""
      return self.consigneAngle - self.angle

   def getCommande(self) :
      """Renvoie une commande pour asservir le moteur en angle.
      La commande est comprise entre -100.0 et +100.0"""
      # A FAIRE : pour l'instant juste proportionnel

      # coeficient proportionnel
      ecartPourMax = pi/2
      coefProportionnel = 1000/ecartPourMax

      # coef integral
      coefIntegral = 1
      self.sommeErreur += self.getEcart()
      if self.sommeErreur > 100 :
         self.sommeErreur = 100
      elif self.sommeErreur < -100 :
         self.sommeErreur = -100

      # calcul de la commande
      commande = (self.getEcart())*coefProportionnel + self.sommeErreur*coefIntegral

      # Traitement du dépassement des valeurs autorisée(-100..100)
      if commande < -100 :
         commande = -100
      elif commande > 100 :
         commande = 100
      else :
         commande = commande

      return commande

   def commander(self, commande) :
      """Commander ce moteur avec une commande.
      Attention, si la pin de sens est activée, l'architecture du pont en H fait que le cycle du PWM est inversé. Il faut donc en tenir compte et inverser le rapport cyclique du PWM"""
      if commande >= 0 :
         GPIO.output(self.pinSens, GPIO.LOW)
         PWM.set_duty_cycle(self.pinPwm, commande)
         self.pwm = commande
         self.sens = 0
      else :
         GPIO.output(self.pinSens, GPIO.HIGH)
         PWM.set_duty_cycle(self.pinPwm, commande + 100)
         self.pwm = -commande
         self.sens = 1

   def majPota(self) :
      """Récupère la valeur du pota"""
      #print ADC.read(self.pinPota)
      self.pota = ADC.read(self.pinPota)
      # attendre 2 ms au minimum pour que l'ADC se fasse correctement
      time.sleep(0.002)

   def majAngle(self) :
      """Transforme la valeur du pota en un angle en fonction des caractéristiques du pota.
      self.pota doit etre à jour !"""
      self.angle = self.angleMin + (self.pota-self.potaMin)*(self.angleMax-self.angleMin)/(self.potaMax-self.potaMin)
