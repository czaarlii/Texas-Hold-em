from treys import Card
import BRVfunctions
import warnings

stan_gracza = {"w_grze": 0,
               "spasowal": -1,
               "czeka": -2,
               "postawil": -3,
               "va bank": -4,
               "dolozyl": -5,
               "skonczyl": -6
               }


class PaczkaDoKlienta:   # do gry po lanie, dane od serwera
    def __init__(self, stol='', akcja='', min=0, maks=0, podbicia=0, odp=False):
        self.akcja_info = akcja
        self.stol_info = stol
        self.min_stawka = min
        self.maks_stawka = maks
        self.liczba_podbic = podbicia
        self.wymagana_odp = odp

    def czysc(self):
        self.akcja_info = ''
        self.stol_info = ''
        self.wymagana_odp = False


class PaczkaDoSerwera:     # dane od klienta
    def __init__(self, odp):
        self.odpowiedz = odp


class Gracz:
    def __init__(self, id):
        self.id = id
        self.reka = [Card(), Card()]
        self.kapital = 1000
        self.stan = stan_gracza["w_grze"]
        self.podbicia = 0

    def wypisz_karty_gracza(self, nr):
        return "Karty gracza %d" % nr + wypisz_karty(self.reka)


class Stol:
    def __init__(self, ilosc_graczy):
        self.karty = [Card()] * 5
        self.odkryte = 3
        self.stawki_graczy = [0] * ilosc_graczy
        self.pula = 0

    def wypisz_karty_na_stole(self):
        return "\nStol: " + wypisz_karty(self.karty[0:self.odkryte])

    def doloz_stawke(self, gracz, stawka):
        gracz.kapital -= stawka
        self.stawki_graczy[gracz.id] += stawka
        if gracz.kapital != 0:
            return "\n***Gracz %d dolozyl do stawki " % (gracz.id+1) + str(stawka) + "***"
        else:
            return '\n***Gracz %d poszedl all-in i dolozyl do stawki ' % (gracz.id+1) + str(stawka) + "!***"

    def zbierz_do_puli(self):
        for i in range(0,2):
            self.pula += self.stawki_graczy[i]
            self.stawki_graczy[i] = 0
        return

############################################################################################


def wypisz_karty(card_ints):
    output = ''

    for i in range(len(card_ints)):
        c = card_ints[i]
        if i != len(card_ints) - 1:
            output += str(Card.int_to_pretty_str(c)) + ","
        else:
            output += str(Card.int_to_pretty_str(c)) + " "
    return output


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
    odp = input("\nNacisnij ENTER aby podjac akcje.")
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
            print("\nNieprawidłowa akcja %s" % odp)


def podejmij_akcje(gracz, akcja, stol):
    if akcja == -1:
        wiadomosc = "\n***Gracz %s spasowal. " % str(gracz.id + 1) + "***"
        gracz.stan = stan_gracza["spasowal"]
    elif akcja == -2:
        wiadomosc = '***Gracz %d czeka.***' % (gracz.id+1)
        gracz.stan = stan_gracza["czeka"]
    elif akcja == -4:
        wiadomosc = stol.doloz_stawke(gracz, gracz.kapital)
        gracz.stan = stan_gracza["va bank"]
    elif akcja == -6:
        wiadomosc = "\n*****************Gracz %s poddał się!" % str(gracz.id + 1), "***************"
        gracz.stan = stan_gracza["skonczyl"]
    else:
        wiadomosc = stol.doloz_stawke(gracz, int(akcja))
        gracz.podbicia += 1
        gracz.stan = stan_gracza["postawil"]
    return wiadomosc


def czy_koniec_tury(gracze, stol, najw_stawka):
    for i in range(0, len(gracze)):
        if not ((najw_stawka == stol.stawki_graczy[i] or gracze[i].stan == stan_gracza["va bank"])
                and (gracze[i].stan == stan_gracza["czeka"] or
                gracze[i].stan == stan_gracza["va bank"] or
                gracze[i].stan == stan_gracza["postawil"])):
            return False
    return True


def czy_wszyscy_spasowali(gracze):  #zwraca idx gracza jedynego w rundzie
    w_grze = -1
    jest_1_w_grze = False

    for i in range(0, len(gracze)):
        if gracze[i].stan != stan_gracza["spasowal"] and gracze[i].stan != stan_gracza["skonczyl"]:
            if jest_1_w_grze:
                return -1
            else:
                w_grze = i
                jest_1_w_grze = True

    return w_grze


def czy_wszyscy_odpadli(gracze):
    pozostal_idx = -1
    pozostalo = 0

    for g in gracze:
        if g.stan != stan_gracza["skonczyl"]:
            pozostal_idx = g.id
            pozostalo += 1

    if pozostalo > 1:
        return -1
    else:
        return pozostal_idx


def czy_ktos_allin(gracze):
    for g in gracze:
        if g.stan == stan_gracza["va bank"]:
            return True
    return False


def liczba_graczy_w_licytacji(gracze):
    i = 0
    for g in gracze:
        if g.stan != stan_gracza["skonczyl"] and g.stan != stan_gracza["va bank"] and g.stan != stan_gracza["spasowal"]:
            i += 1
    return i


def rozdaj_pule(gracze, stol, wyniki):
    if wyniki[0] < wyniki[1]:
        print("\n***Zwyciezca rundy zostaje gracz 1!***")
        gracze[0].kapital += stol.pula
        stol.pula = 0
    elif wyniki[1] < wyniki[0]:
        print("\n***Zwyciezca rundy zostaje gracz 2!***")
        gracze[1].kapital += stol.pula
        stol.pula = 0
    else:
        print("\n***Nastapil remis w tej rundzie.***")
        gracze[0].kapital += stol.pula / 2
        gracze[1].kapital += stol.pula / 2
        stol.pula = 0
    return


def zresetuj_akcje(gracze, do_poczatku=False):    # reset dla nowej rundy
    if do_poczatku:
        for i in range(0, len(gracze)):
            if gracze[i].stan != stan_gracza["skonczyl"]:
                gracze[i].stan = stan_gracza["w_grze"]

            gracze[i].podbicia = 0
    else:
        for i in range(0, len(gracze)):
            if gracze[i].stan != stan_gracza["spasowal"] \
                and gracze[i].stan != stan_gracza["va bank"] \
                    and gracze[i].stan != stan_gracza["skonczyl"]:
                gracze[i].stan = stan_gracza["w_grze"]

            gracze[i].podbicia = 0
    return

