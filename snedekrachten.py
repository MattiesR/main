import utility as ut

#OUTPUT FORMAT SNEDEKRACHTEN: {balk: [[interval, snedekracht], [interval, snedekracht], ...], balk: [[interval, snedekracht], [interval, snedekracht], ...], ...}
def main(Constructie, krachten):
    #returns a list of snedekrachten
    balken = Constructie.get_balken()
    connecties = Constructie.get_connecties()

    snedekrachten = dict()

    for balk in balken:
        connectie_balken = []
        krachten_op_balk = []
        for connectie in connecties:
            if ut.check_connectie_on_balk(balk, connectie):
                connectie_balken.append(connectie)
        for kracht in krachten:
            if ut.check_on_balk(balk, kracht):
                krachten_op_balk.append(kracht)

        berekening = bereken(balk, connectie_balken, krachten_op_balk)
        snedekrachten[balk] = berekening
    return snedekrachten

def bereken(balk, connectie_balken, krachten_op_balk):
    snedekrachten = []
    intervallen = splits_intervallen(balk, connectie_balken, krachten_op_balk)
    start = balk.get_Punten()[0]  # startpunt van balk
    krachten_relevant = []
    for interval in intervallen:
        Normaalkracht = 0
        Dwarskracht = 0
        Moment_const = 0
        Moment_x = 0
        ...
        #krachten_in_interval = []
        for kracht in krachten_op_balk:
            if ut.check_on_interval(interval, kracht) and kracht.Aangrijping != interval[1]:
                krachten_relevant.append(kracht)
        for kracht in krachten_relevant:
            Normaalkracht = Normaalkracht + get_normaalkracht(balk,kracht)
            Dwarskracht = Dwarskracht + get_dwarskracht(balk,kracht)
            Moment_x = Moment_x + ut.cross(balk.unit_vector, kracht.kracht_componenten)    #NOG FIXEN
            Moment_const = Moment_const - get_moment(interval[0],kracht)                    #NOG FIXEN!!!!

        snedekrachten_interval = [interval, Normaalkracht, Dwarskracht, [Moment_const, Moment_x]]
        snedekrachten.append(snedekrachten_interval)

    return snedekrachten

def splits_intervallen(balk, connectie_balken, krachten_op_balk):   #split balk op in intervallen waar nieuwe connectie of kracht op komen
    intervallen = []
    punten = []
    start = balk.get_Punten()[0]    #startpunt van balk
    #eind = balk.get_Punten()[1]     #eindpunt van balk
    for connectie in connectie_balken:
        punten.append(connectie)
    for kracht in krachten_op_balk:
        punten.append(kracht.Aangrijping)
    #punten.append(eind)
    punten = list(set(punten))      #remove duplicates
    sorted_punten = ut.sort_points(start, punten)
    try:
        length_sorted_punten = len(sorted_punten)
    except:
        length_sorted_punten = 0
    for i in range(length_sorted_punten):
        if i < length_sorted_punten-1:
            interval = [sorted_punten[i], sorted_punten[i+1]]
            intervallen.append(interval)
    return intervallen

def get_normaalkracht(balk, kracht):
    normaalkracht = -ut.dot(balk.unit_vector, kracht.kracht_componenten)
    return normaalkracht

def get_dwarskracht(balk, kracht):
    dwarskracht = -ut.dot(balk.normal_vector, kracht.kracht_componenten)
    return dwarskracht

def get_moment(calc_point, kracht):
    moment = 0
    if kracht.Aangrijping == calc_point:
        return moment
    #r = ut.unit_vector(calc_point, kracht.Aangrijping)      #vector van a naar b
    #r = (r[0]*ut.distance(calc_point, kracht.Aangrijping), r[1]*ut.distance(calc_point, kracht.Aangrijping))          #vector van a naar b met lengte
    r = ut.vector(calc_point, kracht.Aangrijping)
    moment = ut.cross(r, kracht.kracht_componenten)
    return moment

def display_snedekrachten_balk(balk, snedekrachten_berekening):
    output = []
    for snedekracht in snedekrachten_berekening:
        if snedekracht == balk:
            snedekracht_info = snedekrachten_berekening[snedekracht]
    intervallen = []
    print("Balk: " + str(balk) + "\n")
    for interval in snedekracht_info:
        info = "Interval: " + str(interval[0][0]) + " - " + str(interval[0][1]) + "\n"
        info = info + "Normaalkracht: " + str(interval[1]) + "\n"
        info = info + "Dwarskracht: " + str(interval[2]) + "\n"
        info = info + "Moment: " + str(interval[3][0]) + " + " + str(interval[3][1]) + "x" + "\n"
        print(info)
        intervallen.append(info)
    output.append(intervallen)
    return snedekracht_info

def display_spanningen_balk(balk, spanningen_berekening):
    output = []
    for snedekracht in spanningen_berekening:
        if snedekracht == balk:
            spanning_info = spanningen_berekening[snedekracht]
    intervallen = []
    print("Balk: " + str(balk) + "\n")
    for interval in spanning_info:
        info = "Interval: " + str(interval[0][0]) + " - " + str(interval[0][1]) + "\n"
        info = info + "Normaalspanning agv normaalkracht: " + str(interval[1]) + "\n"
        info = info + "schuifspanning: " + str(interval[2]) + "\n"
        info = info + "Normaalspanning agv moment: " + str(interval[3][0]) + " + " + str(interval[3][1]) + "x" + "\n"
        print(info)
        intervallen.append(info)
    output.append(intervallen)
    return spanning_info


#input set of dicts of snedekrachten and oplossing van symbolische krachten
#output dict of resulterende waarde snedekrachten
def combine_snedekrachten(snedekrachten, oplossing):
    output = dict()
    aantal_krachten = len(snedekrachten)
    snedekracht_F = snedekrachten[0]

    for balk in snedekracht_F:
        intervallen = []
        j = 0
        while j < len(snedekracht_F[balk]): #loop over intervallen
            interval = []
            interval.append(snedekracht_F[balk][j][0])
            normaalkracht = 0
            dwarskracht = 0
            moment_const = 0
            moment_x = 0
            i = 0
            while i < len(snedekrachten): #data van verschillende krachten in interval
                if i == 0:
                    normaalkracht += snedekrachten[i][balk][j][1]
                    dwarskracht += snedekrachten[i][balk][j][2]
                    moment_const += snedekrachten[i][balk][j][3][0]
                    moment_x += snedekrachten[i][balk][j][3][1]
                elif i != 0:
                    normaalkracht += snedekrachten[i][balk][j][1] * oplossing[i-1]      #oplossing[i-1] omdat eerste kracht in oplossing niet in snedekrachten zit
                    dwarskracht += snedekrachten[i][balk][j][2] * oplossing[i-1]        #oplossing[i-1] omdat eerste kracht in oplossing niet in snedekrachten zit
                    moment_const += snedekrachten[i][balk][j][3][0] * oplossing[i-1]    #oplossing[i-1] omdat eerste kracht in oplossing niet in snedekrachten zit
                    moment_x += snedekrachten[i][balk][j][3][1] * oplossing[i-1]        #oplossing[i-1] omdat eerste kracht in oplossing niet in snedekrachten zit
                i += 1
            moment = [moment_const, moment_x]
            interval.append(normaalkracht)
            interval.append(dwarskracht)
            interval.append(moment)
            intervallen.append([snedekracht_F[balk][j][0], normaalkracht, dwarskracht, moment])
            j += 1

        output[balk] = intervallen
    return output


#input dict of snedekrachten
#output dict of spanningen (zelfde format, maar spanning ipv snedekracht)
def get_spanningen(snedekrachten):
    output = dict()
    for balk in snedekrachten:
        intervallen = []
        j = 0
        while j < len(snedekrachten[balk]):
            interval = []
            interval.append(snedekrachten[balk][j][0])
            normaalspanning_normaalkracht = bereken_normaalspanning(snedekrachten[balk][j][1], "normaal", balk)
            schuifspanning_dwarskracht = bereken_schuifspanning(snedekrachten[balk][j][2], balk)
            normaalspanning_moment_const = bereken_normaalspanning(snedekrachten[balk][j][3][0], "moment", balk)
            normaalspanning_moment_x = bereken_normaalspanning(snedekrachten[balk][j][3][1], "moment", balk)
            j += 1
            interval.append(normaalspanning_normaalkracht)
            interval.append(schuifspanning_dwarskracht)
            interval.append([normaalspanning_moment_const, normaalspanning_moment_x])
            intervallen.append(interval)
        output[balk] = intervallen
    return output



def bereken_normaalspanning(kracht, type, balk):
    normaalspanning = 0
    if type == "normaal":
        normaalspanning = kracht / balk.get_OpperVlakte()                                       #FORMULE NORMAALSPANNING DOOR NORMAALKRACHT

    if type == "moment":
        normaalspanning = kracht * (balk.get_diameter()/2) /balk.get_traagheidsmoment()        #FORMULE NORMAALSPANNING DOOR MOMENT
    return normaalspanning

def bereken_schuifspanning(kracht, balk):
    schuifspanning = kracht * balk.get_statisch_moment()/(balk.get_diameter()*balk.get_traagheidsmoment())         #FORMULE SCHUIFSPANNING VIA JOURAWSKI
    return schuifspanning

#print(combine_snedekrachten([{"a":1, "b":2}, {"a":3, "b":4}, {"a":5, "b":6}],[1, 2, 4]))
test1 = [{"BALK1": [[[(0, 0), (1, 1)], -0.35355339059327373, 0.35355339059327373, [0, 0.35355339059327373]], [[(1, 1), (2, 2)], -0.35355339059327373, 0.35355339059327373, [0.5, 0.35355339059327373]]], "BALK2": [[[(4, 0), (3, 1)], -0.35355339059327373, -0.35355339059327373, [0, -0.35355339059327373]], [[(3, 1), (2, 2)], -0.35355339059327373, -0.35355339059327373, [-0.5, -0.35355339059327373]]], "BALK3": [[[(1, 1), (3, 1)], 0, 0, [0, 0]]]}, {"BALK1": [[[(0, 0), (1, 1)], -0.35355339059327373, -0.35355339059327373, [0, -0.35355339059327373]], [[(1, 1), (2, 2)], 0.35355339059327373, 0.35355339059327373, [-0.5, 0.35355339059327373]]], "BALK2": [[[(4, 0), (3, 1)], -0.35355339059327373, 0.350355339059327373, [0, 0.35355339059327373]], [[(3, 1), (2, 2)], 0.35355339059327373, -0.35355339059327373, [0.5, -0.35355339059327373]]], "BALK3": [[[(1, 1), (3, 1)], 1.0, 0.0, [0, 0.0]]]}, {"BALK1": [[[(0, 0), (1, 1)], -0.35355339059327373, -0.35355339059327373, [0, -0.35355339059327373]], [[(1, 1), (2, 2)], 0.35355339059327373, 0.35355339059327373, [-0.5, 0.35355339059327373]]], "BALK2": [[[(4, 0), (3, 1)], -0.35355339059327373, 0.35355339059327373, [0, 0.35355339059327373]], [[(3, 1), (2, 2)], 0.35355339059327373, -0.35355339059327373, [0.5, -0.35355339059327373]]], "BALK3": [[[(1, 1), (3, 1)], 1.0, 0.0, [0, 0.0]]]}]
test2 = [{"B1": [[["ok"], 1, 4, [3,4]]]}, {"B1": [[["ok"], 14, 40, [30,40]]]}]



#tests voor combine_snedekrachten
assert combine_snedekrachten(test1, [0,0]) == {"BALK1": [[[(0, 0), (1, 1)], -0.35355339059327373, 0.35355339059327373, [0, 0.35355339059327373]], [[(1, 1), (2, 2)], -0.35355339059327373, 0.35355339059327373, [0.5, 0.35355339059327373]]], "BALK2": [[[(4, 0), (3, 1)], -0.35355339059327373, -0.35355339059327373, [0, -0.35355339059327373]], [[(3, 1), (2, 2)], -0.35355339059327373, -0.35355339059327373, [-0.5, -0.35355339059327373]]], "BALK3": [[[(1, 1), (3, 1)], 0, 0, [0, 0]]]}
assert combine_snedekrachten(test2, [10]) == {"B1": [[["ok"], 1+14*10, 4+40*10, [3+30*10,4+40*10]]]}




