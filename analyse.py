import kracht
import balk
import constructie
import snedekrachten
import statica
import utility as ut
import complementaire_energie as ce
import differentiaal as dif

#Maakt eerst volledige analyse
#Daarna kan je deelanalyses opvragen via text input

#krachten: list of list of kracht objects  [[F1, F2, F3], [P1, P2, P3], [H1, H2, H3]]
def main(constructie, krachten):
    balken = constructie.get_balken()
    berekeningen = []

    for kracht in krachten:
        assert statica.is_statisch(constructie, kracht, []), "De constructie is niet statisch"      #Momenten moeten nog geimplementeerd worden
        berekening = snedekrachten.main(constructie, kracht)
        berekeningen.append(berekening)
    energiepotentiaal = ce.total_energy(balken, berekeningen)
    oplossing = dif.differentiaal(energiepotentiaal, len(berekeningen))

    result_snedekracht = snedekrachten.combine_snedekrachten(berekeningen, oplossing)
    spanningen_result = snedekrachten.get_spanningen(result_snedekracht)

    quit = False
    while not quit:
        invoer = input("Voer commando in: ")
        if input == "quit":
            quit = True

        elif invoer == "snedekrachten":
            for balk in balken:
                snedekrachten.display_snedekrachten_balk(balk, result_snedekracht)


        elif invoer == "spanningen":
            for balk in balken:
                snedekrachten.display_spanningen_balk(balk, spanningen_result)


        elif invoer == "potentiaal":
            print(energiepotentiaal)

        elif invoer == "oplossing":
            print(oplossing)

        elif invoer == "berekeningen_raw":
            print(berekeningen)

        elif invoer == "tekening":
            ut.visualize(constructie, krachten[0])

    print("Analyse is succesvol afgesloten")
    return None

