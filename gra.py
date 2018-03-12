import poker
from treys import Evaluator
from treys import Deck


class Ustawienia_gry:
    def __init__(self, liczba_graczy):
        self.liczba_graczy = liczba_graczy
        self.ciemne = 10


class Gra:
    def __init__(self, liczba_graczy=2):
        self.ustawienia = Ustawienia_gry(liczba_graczy)
        self.gracze = []  # lista 2 graczy
        for i in range(0, liczba_graczy):
            self.gracze.append(poker.Gracz(i))

    def uruchom(self):
        sprawdz = Evaluator()
        rozp = 0  # indeks gracza rozpoczynajacego licytacje

        # główna pętla gry
        while (True):
            print("\n*******************************Kolejna runda*********************************")

            talia = Deck()  # talia kart
            stol = poker.Stol(len(self.gracze))

            zwyciezca = -1  # indeks zwycięzcy
            pas = -1

            for g in self.gracze:
                g.reka = talia.draw(2)

            stol.karty = talia.draw(5)

            stol.doloz_stawke(self.gracze[rozp], self.ustawienia.ciemne)  # początkowa stawka na 1. turę
            self.gracze[rozp].stan = poker.stan_gracza["postawil"]
            najwyzsza_stawka = self.ustawienia.ciemne

            # pętla 3 tur
            for tura in range(1, 4):
                print("\n\n**************Trwa tura %s****************" % str(tura))
                print("\nObecnie w puli: ", stol.pula)

                poker.zresetuj_akcje(self.gracze)  # do czyszczenia akcji z poprz. tury poza pasów i ew. allinów
                if tura == 1:
                    aktywny = poker.nastepny(rozp)  # aktywny to indeks gracza aktywnego (aktualnie decydującego) w licytacji
                else:  # a nastepny() to przesunięcie iteratora na nast. gracza
                    aktywny = rozp

                # pętla pozwalająca wykonywać akcje graczy (jeden obrót to decyzja jednego gracza)
                while (True):
                    if self.gracze[aktywny].stan != poker.stan_gracza["va bank"]:  # wyjątek pomijający graczy vabank

                        # wypisywanie info
                        print("\n**************Teraz gracz %s***************" % (aktywny + 1))
                        stol.wypisz_karty_na_stole()
                        self.gracze[aktywny].wypisz_karty_gracza(aktywny + 1)
                        print("\nNajwyższa stawka na stole: ", najwyzsza_stawka)
                        print("Twoja stawka: ", stol.stawki_graczy[aktywny])
                        print("Kapital: ", self.gracze[aktywny].kapital)

                        # wczytanie akcji gracza, więcej w poker.py
                        odp = poker.wczytaj_poprawna_odp(najwyzsza_stawka - stol.stawki_graczy[aktywny],
                                                         self.gracze[aktywny].kapital,
                                                         self.gracze[aktywny].podbicia)
                        # wykonanie wybranej akcji
                        poker.podejmij_akcje(self.gracze[aktywny], odp, stol)

                        if najwyzsza_stawka < stol.stawki_graczy[aktywny]:
                            najwyzsza_stawka = stol.stawki_graczy[aktywny]  # do info o najwyższej postawionej stawce

                    # obsługa spasowania
                    if self.gracze[aktywny].stan == poker.stan_gracza["spasowal"]:
                        print("\n***Gracz %s spasowal. " % str(aktywny + 1), "***")
                        pas = poker.czy_wszyscy_spasowali(self.gracze)
                        if pas != -1:
                            break

                    # obsługa opcji wylączenia gry
                    if self.gracze[aktywny].stan == poker.stan_gracza["skonczyl"]:
                        print("\n*****************Gracz %s poddał się!" % str(aktywny + 1), "***************")
                        zwyciezca = poker.nastepny(aktywny)
                        break

                    # tu jest sprawdzenie czy wszyscy gracze już coś zrobili gdy stawki są sobie równe
                    if poker.czy_koniec_tury(self.gracze, stol, najwyzsza_stawka):
                        break

                    aktywny = poker.nastepny(aktywny)
                # **********************************koniec pętli while()***************************************

                # sprzątanie po skończonej turze
                stol.zbierz_do_puli()  # wszystkie stawki idą do wspólnej puli
                if zwyciezca >= 0 or pas >= 0:
                    break  # gdy któryś z dwóch graczy spasował
                if poker.liczba_graczy_w_licytacji(self.gracze) <= 1:
                    stol.odkryte = 5
                    break
                stol.odkryte += 1
                najwyzsza_stawka = 0
            # **********************koniec pętli z turami***************************************

            if pas >= 0 and not poker.czy_ktos_allin(self.gracze):  # gdy wszyscy spasowali
                print("\n***Zwyciezca rundy zostaje gracz %s!***" % (pas + 1))
                self.gracze[pas].kapital += stol.pula
                stol.pula = 0
            elif zwyciezca == -1:  # tu nastąpi sprawdzanie kart
                print("\n****************Sprawdzenie kart*****************")
                stol.wypisz_karty_na_stole()

                wyniki = []
                print()
                for g in self.gracze:
                    g.wypisz_karty_gracza()
                    wyniki.append(sprawdz.evaluate(stol.karty, g.reka))
                    print("Wynik gracza %d: %s (%d)"
                          % (g.id+1, sprawdz.class_to_string(sprawdz.get_rank_class(wyniki[-1])), wyniki[-1][1]))

                poker.rozdaj_pule(self.gracze, stol, wyniki)

            # całkowity stan kapitału graczy
            print("\nStan kapitalu graczy: ")
            for g in self.gracze:
                print("Gracz %d: %d" % (g.id+1, g.kapital))

            if zwyciezca != -1:
                print("\n***Zwyciezca gry zostaje gracz %d, gratulacje!!!***" % (zwyciezca+1))
                print("\n")
                input("Nacisnij ENTER aby kontynuowac.")
                break
            else:
                # sprawdzenie czy komuś się pieniądze skończyły
                zwyciezca = -1
                if self.gracze[0].kapital == 0:
                    zwyciezca = 2
                elif self.gracze[1].kapital == 0:
                    zwyciezca = 1

                if zwyciezca != -1:
                    print("\n***Zwyciezca gry zostaje gracz %d, gratulacje!!!***" % (zwyciezca+1))
                    print("\n")
                    input("Nacisnij ENTER aby kontynuowac.")
                    break

            input("\nNacisnij ENTER aby kontynuowac.")

            rozp = poker.nastepny(rozp, len(self.gracze))
            poker.zresetuj_akcje(self.gracze, do_poczatku=True)

        return
