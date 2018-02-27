import poker
from treys import Evaluator
from treys import Deck
import warnings
import zasady

warnings.simplefilter("ignore")

poker.BRVfunctions.printad()
zasady.zasadygry()

def main():
    print("Gra Texas Hold'em Poker sterowany głosowo dla 2 graczy. Zapraszamy do gry!")

    gracze = [poker.Gracz(0), poker.Gracz(1)]   # lista 2 graczy
    stol = poker.Stol(2)                        # stol z 5 kartami, stawkami graczy i pulą
    sprawdz = Evaluator()                       # do sprawdzania kombinacji kart

    rozp = 0            #indeks gracza rozpoczynajacego licytacje
    koniec_gry = -1     #zmienna do zakończenia gry
    va_banque = False     #zmienna ustawiana gdy któryś z graczy poszedł Va Banque

    #główna pętla gry
    while(True):
        print("\n*******************************Kolejna runda*********************************")
        talia = Deck()      #talia kart
        zwyciezca = -1      #indeks zwycięzcy
        stol.odkryte = 3

        gracze[0].reka = talia.draw(2)
        gracze[1].reka = talia.draw(2)

        stol.karty = talia.draw(5)
        stol.najwyzsza_stawka = 10

        stol.doloz_stawke(gracze[rozp], stol.najwyzsza_stawka)      # początkowa stawka na 1. turę
        gracze[rozp].stan == poker.stan_gracza["postawil"]

        #pętla 3 tur
        for tura in range(1,4):
            print("\n\n**************Trwa tura %s****************" % str(tura))
            print("\nObecnie w puli: ", stol.pula)

            poker.zresetuj_akcje(gracze)       # do czyszczenia akcji z poprz. tury poza pasów i ew. vabanków
            if tura == 1:
                akt = poker.nastepny(rozp)     # akt to indeks gracza aktywnego (aktualnie decydującego) w licytacji
            else:                              # a nastepny() to przesunięcie iteratora na nast. gracza
                akt = rozp

            #pętla pozwalająca wykonywać akcje graczy (jeden obrót to decyzja jednego gracza)
            while (True):
                if gracze[akt].stan != poker.stan_gracza["va bank"]:    #wyjątek pomijający graczy vabank

                    #wypisywanie info
                    print("\n**************Teraz gracz %s***************" % (akt+1))
                    stol.wypisz_karty_na_stole()
                    gracze[akt].wypisz_karty_gracza(akt + 1)
                    print("\nNajwyższa stawka na stole: ", stol.najwyzsza_stawka)
                    print("Twoja stawka: ", stol.stawki_graczy[akt])
                    print("Kapital: ", gracze[akt].kapital)

                    #wczytanie akcji gracza, więcej w poker.py
                    odp = poker.wczytaj_poprawna_odp(stol.najwyzsza_stawka - stol.stawki_graczy[akt],
                                                     gracze[akt].kapital,
                                                     gracze[akt].podbicia)
                    #wykonanie wybranej akcji
                    poker.podejmij_akcje(gracze[akt], odp, stol)

                    if stol.najwyzsza_stawka < stol.stawki_graczy[akt]:
                        stol.najwyzsza_stawka = stol.stawki_graczy[akt]     #do info o najwyższej postawionej stawce

                if gracze[akt].stan == poker.stan_gracza["va bank"]:
                    va_banque = True

                #obsługa spasowania
                if gracze[akt].stan == poker.stan_gracza["spasowal"]:
                    print("\n***Gracz %s spasowal. " %str(akt+1), "***")
                    zwyciezca = poker.nastepny(akt)
                    break

                #obsługa opcji wylączenia gry
                if gracze[akt].stan == poker.stan_gracza["konczy"]:
                    print("\n*****************Gracz %s poddał się!" %str(akt+1) ,"***************")
                    koniec_gry = poker.nastepny(akt)
                    break

                #tu jest sprawdzenie czy wszyscy gracze już coś zrobili gdy stawki są sobie równe
                if (stol.najwyzsza_stawka == stol.stawki_graczy[0] or
                    gracze[0].stan == poker.stan_gracza["va bank"]) \
                    and (stol.najwyzsza_stawka == stol.stawki_graczy[1] or
                    gracze[1].stan == poker.stan_gracza["va bank"]) \
                    and (gracze[0].stan == poker.stan_gracza["czeka"] or
                    gracze[0].stan == poker.stan_gracza["va bank"] or
                    gracze[0].stan == poker.stan_gracza["postawil"]) \
                    and (gracze[1].stan == poker.stan_gracza["czeka"] or
                    gracze[1].stan == poker.stan_gracza["va bank"] or
                    gracze[1].stan == poker.stan_gracza["postawil"]):
                    break

                akt = poker.nastepny(akt)
            #**********************************koniec pętli while()***************************************

            #sprzątanie po skończonej turze
            stol.zbierz_do_puli()   #wszystkie stawki idą do wspólnej puli
            if zwyciezca >= 0 or koniec_gry >= 0:
                break       # gdy któryś z dwóch graczy spasował
            if va_banque == True:
                stol.odkryte = 5
                break
            stol.odkryte += 1
            stol.najwyzsza_stawka = 0
        #**********************koniec pętli z turami***************************************


        if zwyciezca >= 0:      # gdy któs spasował
            print("\n***Zwyciezca rundy zostaje gracz %s!***" % (zwyciezca+1))
            gracze[zwyciezca].kapital += stol.pula
            stol.pula = 0
        else:                   # tu nastąpi sprawdzanie kart
            print("\n****************Sprawdzenie kart*****************")
            stol.wypisz_karty_na_stole()
            gracze[0].wypisz_karty_gracza(1)
            gracze[1].wypisz_karty_gracza(2)

            wynik1 = sprawdz.evaluate(stol.karty, gracze[0].reka)
            figura1 = sprawdz.get_rank_class(wynik1)

            wynik2 = sprawdz.evaluate(stol.karty, gracze[1].reka)
            figura2 = sprawdz.get_rank_class(wynik2)

            print("\nWynik gracza 1: %s (%d)" % (sprawdz.class_to_string(figura1), wynik1))
            print("Wynik gracza 2: %s (%d)" % (sprawdz.class_to_string(figura2), wynik2))

            if wynik1 < wynik2:
                print("\n***Zwyciezca rundy zostaje gracz 1!***")
                gracze[0].kapital += stol.pula
                stol.pula = 0
            elif wynik2 < wynik1:
                print("\n***Zwyciezca rundy zostaje gracz 2!***")
                gracze[1].kapital += stol.pula
                stol.pula = 0
            else:
                print("\n***Nastapil remis w tej rundzie.***")
                gracze[0].kapital += stol.pula / 2
                gracze[1].kapital += stol.pula / 2
                stol.pula = 0

        #całkowity stan kapitału graczy
        print("\nStan kapitalu graczy: ")
        print("Gracz 1: ", gracze[0].kapital)
        print("Gracz 2: ", gracze[1].kapital)

        #sprawdzenie czy komuś się pieniądze skończyły
        zwyciezca = -1
        if gracze[0].kapital == 0:
            zwyciezca = 2
        elif gracze[1].kapital == 0:
            zwyciezca = 1

        if zwyciezca != -1:
            print("\n***Zwyciezca gry zostaje gracz %d, gratulacje!!!***" % zwyciezca)
            print("\n")
            input("Nacisnij ENTER aby kontynuowac.")
            break
        elif koniec_gry >= 0:
            print("\n***Zwyciezca gry zostaje gracz %s, gratulacje!!!***" % str(koniec_gry+1))
            print("\n")
            input("Nacisnij ENTER aby kontynuowac.")
            break

        input("\nNacisnij ENTER aby kontynuowac.")
        rozp = poker.nastepny(rozp)
        gracze[0].stan = poker.stan_gracza["w_grze"]
        gracze[1].stan = poker.stan_gracza["w_grze"]
        va_banque = False


if __name__ == "__main__":
    main()
