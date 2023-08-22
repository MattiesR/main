import math
import utility as ut
class Balk:
  def __init__(self, Punten, diameter):
    self.Punten = Punten  # list of tuple objects, moeten op een rechte liggen + in volgorde
    self.diameter = diameter

    #attributes
    self.length = ut.length(self.Punten)
    self.oppervlakte = math.pi * (self.diameter/2)**2
    self.traagheidsmoment = math.pi * (self.diameter/2)**4 / 4
    self.unit_vector = ut.unit_vector(self.Punten[0], self.Punten[1])
    self.normal_vector = ut.normal_vector(self.unit_vector)
    self.emodulus = 210000000000  #staal in N/m^2
    self.statisch_moment = self.traagheidsmoment / (self.diameter/2)        #NOG TE BEREKENEN!!!!!
    #checks of valid input
    assert len(Punten) == 2, "Een balk moet 2 punten hebben"

  def get_Punten(self):
    return self.Punten

  def get_length(self):
    return self.length

  def get_OpperVlakte(self):
    return self.oppervlakte

  def get_Emodulus(self):
    return self.emodulus

  def get_traagheidsmoment(self):
    return self.traagheidsmoment

  def get_diameter(self):
    return self.diameter

  def get_statisch_moment(self):
    return self.statisch_moment

  def check_on_balk(self, point):
    #checkt of een punt op de balk ligt
    #point is een tuple met 2 coördinaten
    #returnt True als het punt op de balk ligt, anders False
    return ut.is_between(point, self.Punten[0], self.Punten[1])

  def set_traagheidsmoment(self, traagheidsmoment):
    #set het traagheidsmoment van de balk
    #returnt None
    self.traagheidsmoment = traagheidsmoment
  def set_oppervlakte(self, oppervlakte):
    #set de oppervlakte van de balk
    #returnt None
    self.oppervlakte = oppervlakte

  def set_emodulus(self, emodulus):
    #set de emodulus van de balk
    #returnt None
    self.emodulus = emodulus
