import utility as ut
import math
class Kracht:
  def __init__(self, Aangrijping, kracht_componenten):
    self.Aangrijping = Aangrijping                  #coördinaten van het aangrijpingspunt
    self.kracht_componenten = kracht_componenten    #krachtcomponenten in x en y richting

    #attributes
    self.kracht_grootte = math.sqrt((self.kracht_componenten[0])**2 + (self.kracht_componenten[1])**2)

    #checks of valid input
    assert len(Aangrijping) == 2, "Het aangrijpingspunt moet 2 coördinaten hebben"
    assert len(kracht_componenten) == 2, "De kracht moet 2 componenten hebben"

  def get_Aangrijping(self):
        return self.Aangrijping

  def get_kracht_componenten(self):
        return self.kracht_componenten

  def get_grootte(self):
        return self.kracht_grootte




