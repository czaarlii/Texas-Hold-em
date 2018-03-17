import socket
import pickle
import poker
from treys import Evaluator
from treys import Deck
import warnings
import zasady


class UstawieniaGry:
    def __init__(self, liczba_graczy):
        self.liczba_graczy = liczba_graczy
        self.ciemne = 10





def Main():
    host = "127.0.0.1"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    print('Uruchomiono serwer. \nNasluchiwanie...')
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))

    global_info = "Gra Texas Hold'em Poker sterowany głosowo dla 2 graczy. Zapraszamy do gry!"
    print(global_info)
    conn.send(global_info.encode())


    ustawienia = UstawieniaGry(2)
    gracze = []
    for i in range(0, ustawienia.liczba_graczy):
        gracze.append(poker.Gracz(i))
    sprawdz = Evaluator()
    rozp = 0

    #   0 - idx gracza na serwerze
    #   1 - idx klienta

    # główna pętla gry
    while True:
        global_info = "\n*******************************Kolejna runda*********************************"

        talia = Deck()  # talia kart
        stol = poker.Stol(len(gracze))

        zwyciezca = -1  # indeks zwycięzcy
        pas = -1

        for g in gracze:
            g.reka = talia.draw(2)

        stol.karty = talia.draw(5)

        global_info += '\n' + str(stol.doloz_stawke(gracze[rozp], ustawienia.ciemne))  # początkowa stawka na 1. turę
        gracze[rozp].stan = poker.stan_gracza["postawil"]
        najwyzsza_stawka = ustawienia.ciemne

        print(global_info)
        #paczka_tam.stol_info = global_info
        conn.send(pickle.dumps(poker.PaczkaDoKlienta(global_info)))

        # pętla 3 tur
        for tura in range(1, 4):
            global_info = "\n\n**************Trwa tura %s****************" % str(tura)
            global_info += "\n\nObecnie w puli: " + str(stol.pula)

            poker.zresetuj_akcje(gracze)  # do czyszczenia akcji z poprz. tury poza pasów i ew. allinów
            if tura == 1:
                aktywny = poker.nastepny(
                    rozp)  # aktywny to indeks gracza aktywnego (aktualnie decydującego) w licytacji
            else:  # a nastepny() to przesunięcie iteratora na nast. gracza
                aktywny = rozp

            koniec = False

            print(global_info)
            #paczka_tam.stol_info = global_info
            conn.send(pickle.dumps(poker.PaczkaDoKlienta(global_info)))

            # pętla pozwalająca wykonywać akcje graczy (jeden obrót to decyzja jednego gracza)
            while True:
                global_info = ''

                if gracze[aktywny].stan != poker.stan_gracza["va bank"]:  # wyjątek pomijający graczy vabank

                    # wypisywanie info
                    global_info += "\n**************Teraz gracz %s***************" % (aktywny + 1)
                    global_info += stol.wypisz_karty_na_stole()
                    global_info += '\n' + gracze[aktywny].wypisz_karty_gracza(aktywny + 1)
                    global_info += "\nNajwyższa stawka na stole: " + str(najwyzsza_stawka)
                    global_info += "\nTwoja stawka: " + str(stol.stawki_graczy[aktywny])
                    global_info += "\nKapital: " + str(gracze[aktywny].kapital)

                    if aktywny == 0:
                        print(global_info)

                        # wczytanie akcji gracza, więcej w poker.py
                        odp = poker.wczytaj_poprawna_odp(najwyzsza_stawka - stol.stawki_graczy[aktywny],
                                                         gracze[aktywny].kapital,
                                                         gracze[aktywny].podbicia)
                    else:
                        conn.send(pickle.dumps(poker.PaczkaDoKlienta(stol=global_info,
                                                                     min=najwyzsza_stawka - stol.stawki_graczy[aktywny],
                                                                     maks=gracze[aktywny].kapital,
                                                                     podbicia=gracze[aktywny].podbicia,
                                                                     odp=True)))
                        odp = conn.recv(1024)
                        odp = pickle.loads(odp).odpowiedz

                    # wykonanie wybranej akcji
                    global_info = poker.podejmij_akcje(gracze[aktywny], odp, stol)

                    print(global_info)
                    conn.send(pickle.dumps(poker.PaczkaDoKlienta(akcja=global_info)))

                    if najwyzsza_stawka < stol.stawki_graczy[aktywny]:
                        najwyzsza_stawka = stol.stawki_graczy[aktywny]  # do info o najwyższej postawionej stawce

                # obsługa spasowania
                if gracze[aktywny].stan == poker.stan_gracza["spasowal"]:
                    pas = poker.czy_wszyscy_spasowali(gracze)
                    if pas != -1:
                        koniec = True

                # obsługa opcji wylączenia gry
                if gracze[aktywny].stan == poker.stan_gracza["skonczyl"]:
                    zwyciezca = poker.nastepny(aktywny)
                    koniec = True

                if koniec:
                    break

                # tu jest sprawdzenie czy wszyscy gracze już coś zrobili gdy stawki są sobie równe
                if poker.czy_koniec_tury(gracze, stol, najwyzsza_stawka):
                    break

                aktywny = poker.nastepny(aktywny)
            # **********************************koniec pętli while()***************************************

            # sprzątanie po skończonej turze
            stol.zbierz_do_puli()  # wszystkie stawki idą do wspólnej puli
            if zwyciezca >= 0 or pas >= 0:
                break  # gdy któryś z dwóch graczy spasował
            if poker.liczba_graczy_w_licytacji(gracze) <= 1:
                stol.odkryte = 5
                break
            stol.odkryte += 1
            najwyzsza_stawka = 0
        # **********************koniec pętli z turami***************************************

        global_info = ''

        if pas >= 0 and not poker.czy_ktos_allin(gracze):  # gdy wszyscy spasowali
            global_info = "\n***Zwyciezca rundy zostaje gracz %s!***" % (pas + 1)
            gracze[pas].kapital += stol.pula
            stol.pula = 0
        elif zwyciezca == -1:  # tu nastąpi sprawdzanie kart
            global_info = "\n****************Sprawdzenie kart*****************"
            global_info += stol.wypisz_karty_na_stole()

            wyniki = []
            print()
            for g in gracze:
                g.wypisz_karty_gracza()
                wyniki.append(sprawdz.evaluate(stol.karty, g.reka))
                global_info += "Wynik gracza %d: %s (%d)" \
                      % (g.id + 1, sprawdz.class_to_string(sprawdz.get_rank_class(wyniki[-1])), wyniki[-1][1])

            poker.rozdaj_pule(gracze, stol, wyniki)


        # całkowity stan kapitału graczy
        global_info += "\nStan kapitalu graczy: "
        for g in gracze:
            global_info += "\nGracz %d: %d" % (g.id + 1, g.kapital)

        # if zwyciezca != -1:
        #     global_info += "\n***Zwyciezca gry zostaje gracz %d, gratulacje!!!***" % (zwyciezca + 1)
        #     input("\nNacisnij ENTER aby kontynuowac.")
        #     break
        if zwyciezca == -1:
            # sprawdzenie czy komuś się pieniądze skończyły
            zwyciezca = -1
            if gracze[0].kapital == 0:
                zwyciezca = 2
            elif gracze[1].kapital == 0:
                zwyciezca = 1

        if zwyciezca != -1:
            global_info += "\n\n***Zwyciezca gry zostaje gracz %d, gratulacje!!!***" % (zwyciezca + 1)
            print(global_info)
            conn.send(pickle.dumps(poker.PaczkaDoKlienta(global_info)))
            input("\nNacisnij ENTER aby kontynuowac.")
            break

        print(global_info)
        conn.send(pickle.dumps(poker.PaczkaDoKlienta(global_info)))

        input("\nNacisnij ENTER aby kontynuowac.")

        rozp = poker.nastepny(rozp, len(gracze))
        poker.zresetuj_akcje(gracze, do_poczatku=True)




        # data = conn.recv(1024)
        # if not data:
        #     break
        # data = pickle.loads(data)
        # print("from connected  user: " + str(data.liczby))
        #
        # data.bool = True
        # #data = str(data).upper()
        # print("sending: " + str(data.liczby))
        # conn.send(pickle.dumps(data))

    conn.send(pickle.dumps(poker.PaczkaDoKlienta('\nSerwer zakonczyl polaczenie.')))
    conn.close()
    return

if __name__ == '__main__':
    Main()

# host = '127.0.0.1'
# port = 4000
#
# s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
# s.bind((host, port))
#
# gracze = []
# dzialaj = True
#
# print("Serwer uruchomiony.")
# print('IP: ', host)
# print("Port:", port)
#
# while dzialaj:
#     try:
#         dane, adres = s.recvfrom(1024)
#         dane = dane.decode()
#         if "koniec" in str(dane):
#             dzialaj = False
#         if adres not in gracze:
#             gracze.append(adres)
#
#         print(time.ctime(time.time()), str(adres),": :", str(dane))
#         for gracz in gracze:
#             s.sendto(dane, gracze)
#     except:
#         pass
# s.close()
