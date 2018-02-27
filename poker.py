from treys import Card
import BRVfunctions
import warnings

stan_gracza = {"w_grze": 0,
               "spasowal": -1,
               "czeka": -2,
               "postawil": -3,
               "va bank": -4,
               "dolozyl": -5,
               "konczy": -6
               }


class Gracz:
    def __init__(self, id):
        self.id = id
        self.reka = [Card(), Card()]
        self.kapital = 1000
        self.stan = stan_gracza["w_grze"]
        self.podbicia = 0

    def wypisz_karty_gracza(self, nr):
        print("Karty gracza %d" % nr)
        Card.print_pretty_cards(self.reka)
        return


class Stol:
    def __init__(self, ilosc_graczy):
        self.karty = [Card()] * 5
        self.odkryte = 3
        self.stawki_graczy = [0] * ilosc_graczy
        self.pula = 0
        self.najwyzsza_stawka = 10

    def wypisz_karty_na_stole(self):
        print("\nStol: ")
        Card.print_pretty_cards(self.karty[0:self.odkryte])
        return

    def doloz_stawke(self, gracz, stawka):
        gracz.kapital -= stawka
        self.stawki_graczy[gracz.id] += stawka
        print("\n***Gracz %s dolozyl do stawki " %str(gracz.id+1), stawka, "***")
        return

    def zbierz_do_puli(self):
        for i in range(0,2):
            self.pula += self.stawki_graczy[i]
            self.stawki_graczy[i] = 0
        return

############################################################################################

def nastepny(n, max = 2):       #do iteracji
    n += 1
    if (n >= max):
        n = 0
    return n


# zbiór wszystkich komend
def sprawdz(n):     # do wczytania poprawnej odpowiedzi
    return{
        'Pass': -1,
        'Czekam': -2,
        'Stawiam': -3,
        'Va': -4,   #'Va banque'
        'Dokladam': -5,
        'Koniec': -6
    }.get(n,0)


def wczytaj_odp(czy_mozna_podbic):      # tu będzie nasza funkcja głosowa, najważniejsza część projektu :)
    print("\n")
    odp = input("Nacisnij ENTER aby podjac akcje.")
    with warnings.catch_warnings():
        if czy_mozna_podbic:
            odp = BRVfunctions.getreply_canraise()
        else:
            odp = BRVfunctions.getreply_cannotraise()
    return odp.split()


def wczytaj_poprawna_odp(min_stawka, maks_stawka, ilosc_podbic):  #funkcja wczytująca odp. gracza i sprawdzająca poprawność danych
    while True:
        odp = wczytaj_odp(ilosc_podbic < 2)     # w tym miejscu nastąpi wczytanie głosowe danych w postaci stringa, ew 2 jeśli jest stawka
        wart = sprawdz(odp[0])

        if wart != 0:
            if wart == -3:
                if ilosc_podbic >= 2:
                    print("\nJuż zrobiłeś 2 podbicia. Nie możesz więcej.")
                elif int(odp[1]) >= min_stawka and int(odp[1]) <= maks_stawka:
                    return odp[1]
                else:
                    print("\nNieprawidlowa kwota.")

            elif wart == -2 and min_stawka > 0:
                print("\nMusisz cos postawic.")
            elif wart == -5:
                if min_stawka > maks_stawka:
                    print("\nNiewystarczajaco pieniedzy.")
                elif min_stawka == 0:
                    print("\nNic nie musisz dokladac.")
                else:
                    return min_stawka
            else:
                return wart

        else:
            print("\nNieprawidłowa akcja %s" %odp)


def podejmij_akcje(gracz, akcja, stol):
    if akcja == -1:
        gracz.stan = stan_gracza["spasowal"]
    elif akcja == -2:
        gracz.stan = stan_gracza["czeka"]
    elif akcja == -4:
        stol.doloz_stawke(gracz, gracz.kapital)
        gracz.stan = stan_gracza["va bank"]
    elif akcja == -6:
        gracz.stan = stan_gracza["konczy"]
    else:
        stol.doloz_stawke(gracz, int(akcja))
        gracz.podbicia += 1
        gracz.stan = stan_gracza["postawil"]
    return


def zresetuj_akcje(gracze):       #reset dla nowej rundy
    for i in range(0, len(gracze)):
        if gracze[i].stan != stan_gracza["spasowal"] and gracze[i].stan != stan_gracza["va bank"] :
            gracze[i].stan = stan_gracza["w_grze"]
        gracze[i].podbicia = 0
    return

