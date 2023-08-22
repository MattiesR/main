import utility as ut



def is_statisch(constructie, krachten, momenten):
    #returns True if the constructie is static
    #input: Constructie object, list of Kracht objects
    #output: boolean
    #check if the sum of the krachten is zero
    if not som_krachten_is_nul(krachten):
        return False

    #check if the sum of the moments is zero
    if not som_momenten_is_nul(constructie, krachten, momenten):
        return False
    return True


def som_krachten(krachten):
    #returns the sum of the krachten
    #input: list of Kracht objects
    #output: Kracht object
    x = 0
    y = 0
    for kracht in krachten:
        x += kracht.kracht_componenten[0]
        y += kracht.kracht_componenten[1]
    return (x,y)

def som_krachten_is_nul(krachten):
    #returns True if the sum of the krachten is zero
    #input: list of Kracht objects
    #output: boolean
    return som_krachten(krachten) == (0,0)

def som_momenten(constructie, krachten, momenten):
    #returns the sum of the moments
    #input: Constructie object, list of Kracht objects
    #output: float
    som = 0
    balken = constructie.get_balken()
    balk1 = balken[0]
    punt1 = balk1.Punten[0]
    for kracht in krachten:
        som += moment_om_punt(punt1, kracht)
    for moment in momenten:
        som += moment.get_grootte()
    return som

def som_momenten_is_nul(constructie, krachten, momenten):
    #returns True if the sum of the moments is zero
    #input: Constructie object, list of Kracht objects
    #output: boolean
    return som_momenten(constructie, krachten, momenten) == 0

def moment_om_punt(punt, kracht):
    #returns the moment of a kracht around a point
    #input: tuple object, Kracht object
    #output: float
    return ut.cross(ut.vector(punt, kracht.Aangrijping), kracht.kracht_componenten)