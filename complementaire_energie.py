#input snedekrachten

#potentiaal energie via kwadraten momentenlijn en normaalkrachten
#format voor snedekrachten

"""
normaalkrachten = [F, P, H, G]
"""
import utility as ut

"""
momenten = [[F, F*x], [P, P*x], [H, H*x], [G, G*x]]
"""

"""
format voor M^2:
M^2 = [[[FF, FF*x], [FP, FP*x], [FH, HH*x], [FG, GG*x]], [[PP, PP*x], [PH, PH*x], [PG, PG*x]], [[HH, HH*x], [HG, HG*x]], [[GG, GG*x]]
"""

"""
format voor N^2:
N^2 = [[FF, FP, FH, FG], [PP, PH, PG], [HH, HG], [GG]]
"""
#Berekent de complementaire energie in een interval van een balk
#OM totale complementaire energie te berekenen moet je dit voor alle balken doen en dan de som nemen
#input: balk, interval, berekeningen


#FORMAT van berekeningen:
#berekeningen = [berekening1, berekening2, berekening3, ...]
#berekening = {balk1: {interval1: [normaalkracht, dwarskracht, moment], interval2: [normaalkracht, moment], ...}, balk2: {interval1: [normaalkracht, moment], interval2: [normaalkracht, moment], ...}, ...}
#moment = [F, F*x]
#INPUT: balken, gehele lijst van berekeningen (superpositie van reële en symbolische krachten)
def total_energy(balken, snedekrachten_totaal):
    total_energy = []
    aantal_krachten = len(snedekrachten_totaal)

    for balk in balken:
        aantal_interval = len(snedekrachten_totaal[0][balk])  # ELK SNEDEKRACHTEN OBJECT MOET ZELFDE LENGTE VAN INTERVAL HEBBEN!!!
        opp = balk.get_OpperVlakte()
        lengte = balk.get_length()
        emodulus = balk.get_Emodulus()
        traagheidsmoment = balk.get_traagheidsmoment()
        for interval in range(aantal_interval):
            lengte_interval = ut.length(snedekrachten_totaal[0][balk][interval][0])
            normaalkracht = []
            moment = []
            for snedekracht in snedekrachten_totaal:  # gaat zoeken in elke berekening naar de snedekracht bij behorende balk en interval
                normaalkracht.append(snedekracht[balk][interval][1])
                moment.append(snedekracht[balk][interval][3])
            energy = energy_interval(normaalkracht, moment, lengte_interval, opp, emodulus, traagheidsmoment)
            total_energy = ut.add_lists(total_energy, energy)
    return total_energy

#input: format
"""
format voor N^2:
N^2 = [[FF, FP, FH, FG], [PP, PH, PG], [HH, HG], [GG]]
"""

"""
format voor M^2:
M^2 = [[FF,FF*x,FP, FP*x, FH, FH*x], [(Fx)^2, Fx*P, FxPx, Fx*H, FH*x^2], [P^2, P^2*x,PH,PH*x], [(Px)^2, Px*H, PxHx], [H^2, H^2*x], [(Hx)^2]]
"""


def square_normaalkracht(normaalkracht):    #VERIFIED
    square = []
    aantal_soorten_krachten = len(normaalkracht)
    for i in range(aantal_soorten_krachten):
        hulp = []
        j = i
        while j < aantal_soorten_krachten:
            if i == j:
                hulp.append(normaalkracht[i] * normaalkracht[j])
            elif i != j:
                hulp.append((normaalkracht[i] * normaalkracht[j])*2)
            j += 1
        square.append(hulp)
    return square


def square_moment(moment):
    square = []
    momenten_extracted = []
    momenten_extracted = ut.extract(moment)
    for i in range(len(momenten_extracted)):
        hulp = []
        j = i
        while j < len(momenten_extracted):
            if i == j:
                hulp.append(momenten_extracted[i] * momenten_extracted[j])
            elif i != j:
                hulp.append((momenten_extracted[i] * momenten_extracted[j])*2)
            j += 1
        square.append(hulp)
    square = rearrange(square)
    return square


def integrate_normaalkracht_squared(normaalkracht_squared, lengte_interval):
    integrated = []
    for i in normaalkracht_squared:
        for j in i:
            integrated.append(j*lengte_interval)
    return integrated


def integrate_moment_squared(moment_squared, lengte_interval):  #VERIFIED
    integrated = []
    for i in moment_squared:
        sum = 0
        sum += i[0]*lengte_interval
        sum += i[1]*lengte_interval**2/2
        sum += i[2]*lengte_interval**3/3
        integrated.append(sum)
    return integrated


#total energy matrix of one interval
def energy_interval(normaalkracht, moment, lengte_interval, opp, emodulus, traagheidsmoment):   #VERIFIED
    total_energy = []
    normaalkracht_squared = square_normaalkracht(normaalkracht)
    moment_squared = square_moment(moment)

    integrated_normaalkracht_squared = integrate_normaalkracht_squared(normaalkracht_squared, lengte_interval)
    integrated_moment_squared = integrate_moment_squared(moment_squared, lengte_interval)

    for i in range(len(integrated_normaalkracht_squared)):
        amount = 0
        amount += 1/2*integrated_normaalkracht_squared[i]/(opp*emodulus)
        amount += 1/2*integrated_moment_squared[i]/(traagheidsmoment*emodulus)
        total_energy.append(amount)
    return total_energy



#input: format van M^2 kwadraat van sommen
"""
format voor M^2:
M^2 = [[FF,FF*x,FP, FP*x, FH, FH*x], [(Fx)^2, Fx*P, FxPx, Fx*H, FH*x^2], [P^2, P^2*x,PH,PH*x], [(Px)^2, Px*H, PxHx], [H^2, H^2*x], [(Hx)^2]]
"""
#output: format van M^2 gesorteerd per combinatie van krachten
#collecting zelfde combinatie van krachten
"""
format:
M^2 = [[FF, FFx, FFx^2], [FP, FPx, FPx^2], [FH, FHx, FHx^2], [PP, PPx, PPx^2], [PH, PHx, PHx^2], [HH, HHx, HHx^2]]
"""
def rearrange(moment_squared):  #verified
    rearranged = []
    i = 0
    k = 0
    count = 0
    while count < len(moment_squared) :
        i = 0
        while i < len(moment_squared[count]):
            hulp = []
            if i == 0:
                hulp.append(moment_squared[count][i])
                hulp.append(moment_squared[count][i+1])
                hulp.append(moment_squared[count+1][0])
            elif i % 2 == 0:
                hulp.append(moment_squared[count][i])
                hulp.append(moment_squared[count][i+1]+moment_squared[count+1][i-1])
                hulp.append(moment_squared[count+1][i])
            i += 2
            rearranged.append(hulp)
        count += 2
    return rearranged
