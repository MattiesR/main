
class Moment:
  def __init__(self, Aangrijping, moment_grootte):
    self.Aangrijping = Aangrijping                  #coördinaten van het aangrijpingspunt
    self.moment_grootte = moment_grootte            #grootte van moment

    #checks of valid input
    assert len(Aangrijping) == 2, "Het aangrijpingspunt moet 2 coördinaten hebben"
    assert type(moment_grootte) == float or type(moment_grootte) == int , "Het moment moet 1 getal zijn"

  def get_Aangrijping(self):
        return self.Aangrijping

  def get_grootte(self):
        return self.moment_grootte




